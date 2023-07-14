import logging
import time

from fastapi import APIRouter

from proqa_ai.controllers.text import buffer
from proqa_ai.schemas.text import TextRequest, TextResponse

router = APIRouter()
logger = logging.getLogger("proqa_ai")


@router.post("/text", response_model=TextResponse)
async def text(request: TextRequest):
    """
    Generate text from prompt.

    Args:
        request (TextRequest): Text request.
        background_tasks (BackgroundTasks): Background tasks to be run.
    Returns:
        TextResponse: Text response.
    """

    rcv_time = time.time()
    buffer.put((request, rcv_time))
    logger.info("Queued text generation for message %s", request.message_id)

    return TextResponse(
        prompt=request.prompt,
        message_id=request.message_id,
        model_settings=request.model_settings,
        streaming_settings=request.streaming_settings,
    )
