"""
Class for making API calls to the tokenize endpoint of the AI service
"""
import requests
from requests import Response
from django.conf import settings
from api.utils.aiservice import AIServiceAdapter

class TokenizeAdapter(AIServiceAdapter):
    """
    Functions for making API calls to the tokenize service
    """

    def _make_request(self, text: str) -> Response:
        """
        Makes a request to the tokenize service

            Args:
                text (str): Text to tokenize
            Returns:
                Response: Response from the API
        """
        return requests.post(
            settings.AI_SERVICE_URL + self._get_endpoint(),
            json={'text': text},
            timeout=5
        )

    def _convert_response(self, response: Response) -> int:
        """
        Converts a tokenization Response to a Python list and string

            Args:
                response (Response): API response to convert
            Returns:
                int: Resulting number of tokens
        """
        response_json = response.json()
        num_tokens = response_json['num_tokens']
        return num_tokens

    def _get_endpoint(self) -> str:
        """
        Getter for tokenize endpoint

            Returns:
                str: Endpoint
        """
        return "tokenize"

    def get(self, text: str) -> int:
        """
        Makes request to tokenize API converts to Python objects

            Args:
                text (str): Text to tokenize
            Returns:
                int: Resulting number of tokens
        """
        response = self._make_request(text=text)
        return self._convert_response(response=response)
