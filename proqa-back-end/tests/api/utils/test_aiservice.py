"""
Test cases for api/utils/aiservice.py
"""
from django.test import TestCase
from api.utils.aiservice_text import TextAdapter
from api.utils.aiservice_embedding import EmbeddingAdapter
from api.utils.aiservice import PromptBuilder
from api.models import PromptTemplate
from tests.api.resources import constants as c


class TestAIServiceUtils(TestCase):
    """
    Test cases for api/views/aiservice.py
    """

    def setUp(self):
        self.embedding_adapter = EmbeddingAdapter()
        self.text_adapter = TextAdapter()
        # Pass in a mock tokenizer.
        self.prompt_template = PromptTemplate(
            name="test",
            instruction=c.TEST_INSTRUCTION,
            question_format=c.TEST_QUESTION_FORMAT,
            answer_format=c.TEST_ANSWER_FORMAT
        )

        self.prompt_builder = PromptBuilder(
            self.prompt_template, lambda text: len(text.split()))

    def test_embedding_convert_response(self):
        """
        Tests _convert_respose from EmbeddingAdapter
        """
        response = c.TEST_EMBEDDING_RESPONSE
        text, embedding = self.embedding_adapter._convert_response(response)
        self.assertEqual(text, response.json()['text'])
        self.assertEqual(embedding, response.json()['embedding'])

    def test_prompt_builder(self):
        """
        Tests PromptBuilder
        """
        prompt = self.prompt_builder.get_prompt(
            c.TEST_MESSAGES, c.TEST_QUESTION,
            c.TEST_CONTEXT
        )
        self.assertEqual(prompt, c.TEST_PROMPT)
