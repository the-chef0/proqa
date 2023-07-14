import logging
import time
from queue import Queue

import requests

from proqa_ai.server.config import settings
from proqa_ai.utilities.model_manager import ModelManager, StreamingCallbackHandler

logger = logging.getLogger("proqa_ai")
model_manager = ModelManager()
buffer = Queue()

def generate_text_worker():
    """
    The worker that generates text from the prompt.
    """
    logger.info("Starting text generation worker.")
    while True:
        item = buffer.get()
        if item is None:
            break

        request, rcv_time = item
        if time.time() - rcv_time > settings.text_generation_timeout:
            logger.warning("Text generation timed out for message %s", request.message_id)
            _end_stream(
                request.streaming_settings.channel,
                request.streaming_settings.session_id,
                request.message_id
            )
            continue

        logger.info("Generating text for message %s", request.message_id)
        generated_text = model_manager.generate_text(
            request.prompt, request.message_id, request.model_settings, request.streaming_settings
        )
        _post_text(generated_text, request.streaming_settings.session_id)
        logger.info("Posted text for message %s", request.message_id)

    logger.info("Stopping text generation worker.")


def _post_text(text: str, session_id: str):
    """
    Post the generated text to the backend.

    Args:
        text (str): Generated text.
        session_id (str): ID of the session to stream to
    """
    requests.post(
        f'{settings.backend_http_url}/api/answer/',
        json={'answer': text, 'session_id': session_id},
        timeout=30
    )

def _end_stream(channel: str, session_id: str, message_id: str):
    """
    End the stream in case of timeout.

    Args:
        channel (str): Channel to stream to.
        session_id (str): ID of the session to stream to.
        message_id (str): ID of the answer.
    """
    streaming_handler = StreamingCallbackHandler(
        channel, session_id, message_id
    )
    streaming_handler.on_llm_new_token("[TIMEOUT]")
    streaming_handler.on_llm_end()
