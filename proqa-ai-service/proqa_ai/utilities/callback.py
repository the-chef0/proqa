import json
import urllib.parse
import requests
from langchain.callbacks.base import BaseCallbackHandler

from proqa_ai.server.config import settings


class StreamingCallbackHandler(BaseCallbackHandler):
    """
    Callback handler for streaming LLM responses to pushpin.
    """

    def __init__(self, channel: str, session_id: str, message_id: str):
        """
        Args:
            channel (str): Channel name.
            session_id (str): Identifier of the current chat session of the question.
            message_id (str): Identifier of the current answer being generated.
        """
        self.channel = channel
        self.session_id = session_id
        self.message_id = message_id
        self.url = f"{settings.pushpin_http_url}/publish"
        self._id = 0

    def on_llm_start(self, *args, **kwargs):
        """
        Pushes a [START] token to indicate start of stream.
        """
        payload = self._create_payload("[START]")
        self._send_event(payload)

    def on_llm_new_token(self, token: str, **kwargs):
        """
        For each token, it pushes the corresponding payload to pushpin.

            Args:
                token (str): token used in the payload.
        """
        payload = self._create_payload(token)
        self._send_event(payload)

    def on_llm_end(self, *args, **kwargs):
        """
        Pushes a [END] token to indicate end of stream.
        """
        payload = self._create_payload("[END]")
        self._send_event(payload)

    def _create_payload(self, token: str) -> str:
        """
        Creates the payload to send on each new token.

            Args:
                token (str): token to create payload with.
            Returns:
                str: generated payload in json format.
        """
        token = urllib.parse.quote(token)
        payload = {
            "token": token,
            "messageID": self.message_id,
            "sessionID": self.session_id,
        }

        data = {
            "channel": self.channel,
            "id": f'{self.message_id}-{self._id}',
            "formats": {
                "http-stream": {
                    "content": f"event:message\ndata:{payload}\n\n",
                }
            }
        }
        if self._id > 0:
            data["prev_id"] = f'{self.message_id}-{self._id-1}'
        self._id += 1

        json_data = json.dumps({"items": [data]})
        return json_data

    def _send_event(self, payload: str):
        headers = {"Content-Type": "application/json"}
        requests.post(self.url, data=payload, headers=headers, timeout=1)
