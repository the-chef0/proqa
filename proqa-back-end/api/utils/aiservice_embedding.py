"""
Class for making API calls to the embedding endpoint of the AI service
"""
from typing import Tuple
import requests
from requests import Response
import numpy as np
from django.conf import settings
from api.utils.aiservice import AIServiceAdapter

class EmbeddingAdapter(AIServiceAdapter):
    """
    Functions for making API calls to the embedding service
    """

    def _make_request(self, text: str) -> Response:
        """
        Makes a request to the embedding service

            Args:
                text (str): Text to make embedding from
            Returns:
                Response: Response from the API
        """
        return requests.post(
            settings.AI_SERVICE_URL + self._get_endpoint(),
            json={'text': text},
            timeout=30
        )

    def _convert_response(self, response: Response) -> Tuple[list, str]:
        """
        Converts an embedding Response to a Python vector and string

            Args:
                response (Response): API response to convert
            Returns:
                list: Resulting embedding
                str: Original text
        """
        response_json = response.json()
        text = response_json['text']
        embedding = response_json['embedding']
        return text, embedding

    def _get_endpoint(self) -> str:
        """
        Getter for embedding endpoint
        """
        return 'embedding'

    def get(self, text: str) -> Tuple[list, str]:
        """
        Makes request to embedding API and converts to Python objects

            Args:
                text (str): Text to make embedding from
            Returns:
                list: Resulting embedding
                str: Original text
        """
        response = self._make_request(text=text)
        return self._convert_response(response=response)

    def batch_get(self, messages: list, last_question: str) -> list:
        """
        Makes multiple requests to embedding API and converts to Python objects

            Args:
                messages (list): Messages to make embeddings from (only questions)
                last_question (str): The question that was last asked
                decay_scalar (float): The ratio by which each question is less relevant
                compared to its successor
            Returns:
                list: Resulting weighted embedding given the texts 
        """
        decay_scalar = settings.DECAY_SCALAR

        # get list of all questions
        texts = [message['content'] for message in messages if not message['is_answer']]
        texts.append(last_question)

        # get normalized weights for given decay_scalar
        weights = np.array([pow(decay_scalar, i) for i in range(len(texts))][::-1])
        weights *= 1.0 / np.linalg.norm(weights, ord=1)

        embeddings = []
        for (text, weight) in zip(texts, weights):
            response = self._make_request(text=text)
            _, embedding = self._convert_response(response=response)
            embeddings.append(np.array(embedding) * weight)
        return np.sum(embeddings, axis=0).tolist()
