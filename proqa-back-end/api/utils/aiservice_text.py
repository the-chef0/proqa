"""
Class for making API calls to the embedding endpoint of the AI service
"""
import requests
from requests import Response
from django.conf import settings
from api.utils.aiservice import AIServiceAdapter
from api.models import LLM

class TextAdapter(AIServiceAdapter):
    """
    Functions for making API calls to the text generation service
    """

    def __init__(self):
        self.model = None

    def _make_request(self, channel: str, prompt: str, session_id: str, message_id: str
                      ) -> Response:
        """
        Schedules the generation of text from the AI service.

            Args:
                channel (str): Channel to stream text to
                prompt (str): Prompt to generate from
                session_id (str): ID of the session to stream to
                message_id (str): ID of the answer
            Returns:
                Response: Response from the API
        """
        return requests.post(
            settings.AI_SERVICE_URL + self._get_endpoint(),
            json={
                "prompt": prompt,
                "message_id": message_id,
                "model_settings": {
                    "model_name": self.model.name,
                    "n_ctx": self.model.context_size,
                    "temperature": self.model.temperature,
                    "n_gpu_layers": self.model.gpu_layers,
                    "n_batch": self.model.batch_size
                },
                "streaming_settings": {
                    "channel": channel,
                    "session_id": session_id
                }
            },
            timeout=5
        )

    def _convert_response(self, response: Response) -> int:
        """
        Converts a text generation Response to a Python int

            Args:
                response (Response): API response to convert
            Returns:
                int: Status code
        """
        return response.status_code

    def _get_endpoint(self) -> str:
        """
        Getter for text endpoint
        """
        return 'text'

    def get(self, channel: str, prompt: str, session_id: str, message_id: str) -> int:
        """
        Makes request to text generation API converts to Python objects

            Args:
                channel (str): Channel to stream text to
                prompt (str): Prompt to generate from
                session_id (str): ID of the session to stream to
                message_id (str): ID of the answer
            Returns:
                int: Status code
        """
        response = self._make_request(channel=channel,
                                      prompt=prompt,
                                      session_id=session_id,
                                      message_id=message_id)
        return self._convert_response(response=response)

    def update_model(self, model: LLM):
        """
        Checks if the given model is the same as the used model. If not, then updates it.

            Args:
                model (LLM): model to check.
        """
        self.model = model
