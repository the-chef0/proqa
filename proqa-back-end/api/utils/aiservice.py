"""
Functions for making API calls to the AI service
"""
from abc import ABC, abstractmethod
from collections import deque
from requests import Response
from api.models import PromptTemplate

class AIServiceAdapter(ABC):
    """
    Abstract class for making API calls to an AI service
    """

    @abstractmethod
    def _make_request(self, *args, **kwargs) -> Response:
        """
        Abstract request maker
        """

    @abstractmethod
    def _convert_response(self, *args, **kwargs) -> tuple:
        """
        Abstract converter of API reponse to Python objects
        """

    def _get_endpoint(self) -> str:
        """
        Abstract getter for specific endpoint
        """

    @abstractmethod
    def get(self, *args, **kwargs) -> tuple:
        """
        Abstract controler to make a request and return Python objects
        """

class PromptBuilder:
    """
    Builds prompts for the AI service.
    """

    def __init__(
            self, prompt_template: PromptTemplate, tokenizer: callable,
            max_tokens: int = 2048
    ):
        """
        Args:
            prompt_template (PromptTemplate): Template used for building the prompt
            tokenizer (callable): Tokenizer for instruction that accepts str and returns list of 
            tokens.
            max_tokens (int): Maximum number of tokens in prompt.
        """
        self.instruction = prompt_template.instruction.strip()
        self.question_format = prompt_template.question_format.strip()
        self.answer_format = prompt_template.answer_format.strip()
        self.separator = prompt_template.separator

        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def get_prompt(self, messages: list, question: str, context: str) -> str:
        """
        Fills prompt template in conversational format.

            Args:
                messages (list): List of messages in the chat session as returned by
                                 `get_raw_messages()` in `chat_session.py`
                question (str): Question to ask AI service
                context (str): Context with which to answer the question.
            Returns:
                str: Prompt for AI service
        """
        messages = self._parse_messages(messages)
        question = self._get_question(question, context)
        answer = self._get_answer("", False)

        num_tokens = self.tokenizer(
            self.instruction) + self.tokenizer(answer) + self.tokenizer(question)

        # try to use only 90% of the context window in case of precision errors
        upperbound = self.max_tokens * 0.9
        history = deque()
        for message in reversed(messages):
            token_count = self.tokenizer(message)
            if num_tokens + token_count > upperbound:
                break
            history.appendleft(message)
            num_tokens += token_count
        history = "\n".join(history)

        prompt = f"\n{self.instruction}\n\n{history}\n{question}\n{answer}\n"

        return prompt

    def _get_question(self, question: str, context: str) -> str:
        """
        Formats question for prompt.

            Args:
                question_format (str): Template used for question formatting
                question (str): Question plaintext
                context (str): Context plaintext

            Returns:
                str: Formatted question block given the question template.
        """
        return self.question_format.format(question=question, context=context)

    def _get_answer(self, answer: str, separator: bool = True) -> str:
        """
        Formats answer for prompt.

            Args:
                answer_format (str): Template used for answer formatting
                answer (str): Answer plaintext
                separator (bool): Whether to add separator at the end of answer or not

            Returns:
                str: Formatted answer given the answer template.
        """
        return self.answer_format.format(answer=answer) + (self.separator if separator else "")

    def _parse_messages(self, messages: list) -> list:
        """
        Parses the messages into a list of tuples of the form (message, num_tokens).
        Also formats the messages for the prompt.

            Args:
                messages (list): List of messages in the chat session as returned by
            Returns:
                list: List of tuples of the form (message, num_tokens).
        """
        parsed_messages = []
        for message in messages:
            if message['is_answer']:
                text = self._get_answer(message['content'])
            else:
                text = self._get_question(message['content'], message['context'])

            parsed_messages.append(text)
        return parsed_messages
