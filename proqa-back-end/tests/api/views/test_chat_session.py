import uuid
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from api.views.chat_session import (
    creation,
    deletion,
    hiding,
    pinning,
    rating,
    history,
    messages
)
from api.models import (
    ChatSession,
    Question,
    Answer,
    Chunk,
    Source,
    Collection
)
from tests.api.resources import constants as c

class TestAIServiceViews(TestCase):
    """
    Test class for AI service endpoints.
    """
    def setUp(self):
        """
        Set up
        """
        self.user = User.objects.create_user(
            username="testuser",
        )
        self.chat_session = ChatSession.objects.create(
            author=self.user,
        )
        self.collection = Collection.objects.create(
            name="testcollection",
        )
        self.source = Source.objects.create(
            collection=self.collection,
            file_name="",
            file_type='pdf'
        )
        self.chunk = Chunk.objects.create(
            source=self.source,
            content="",
            times_referenced=1
        )
        self.question = Question.objects.create(
            session=self.chat_session,
            content=c.TEST_QUESTION
        )
        self.answer = Answer.objects.create(
            question=self.question,
            session=self.chat_session,
            context=self.chunk
        )
    def __get_test_response(self, path: str, method: callable, data: dict):
        """
        Gets response from specified endpoint
        """
        request = RequestFactory().post(
            path=path,
            data=data
        )
        request.user = self.user
        response = method(request)
        return response

    def test_creation(self):
        """
        Tests the chat/creation endpoint
        """
        response = self.__get_test_response(
            path='/chat/creation/',
            method=creation,
            data={'title': '', 'color':''}
        )
        self.assertEqual(type(response.data['id']), uuid.UUID)

    def test_deletion(self):
        """
        Tests the chat/deletion endpoint
        """
        response = self.__get_test_response(
            path='/chat/deletion/',
            method=deletion,
            data={'chat_session_id': self.chat_session.session_id}
        )
        self.assertEqual(response.data, {"status": "deleted"})

    def test_hiding(self):
        """
        Tests the chat/hiding endpoint
        """
        response = self.__get_test_response(
            path='/chat/hiding/',
            method=hiding,
            data={'chat_session_id': self.chat_session.session_id, 'hide': True}
        )
        self.assertEqual(response.data, {"status": "hidden"})

    def test_pinning(self):
        """
        Tests the chat/pinning endpoint
        """
        response = self.__get_test_response(
            path='/chat/pinning/',
            method=pinning,
            data={'chat_session_id': self.chat_session.session_id, 'pin': True}
        )
        self.assertEqual(response.data, {"status": "pinned"})

    def test_rating(self):
        """
        Tests the chat/rating endpoint
        """
        response = self.__get_test_response(
            path='/chat/rating/',
            method=rating,
            data={'answer_id': self.answer.answer_id, 'rating': 1}
        )
        self.assertEqual(response.data, {"status": "rated"})

    def test_history(self):
        """
        Tests the chat/history endpoint
        """
        response = self.__get_test_response(
            path='/chat/history/',
            method=history,
            data={}
        )
        self.assertEqual(response.data['chats'][0]['session_id'], self.chat_session.session_id)

    def test_messages(self):
        """
        Tests the chat/messages endpoint
        """
        response = self.__get_test_response(
            path='/chat/messages/',
            method=messages,
            data={'session': self.chat_session.session_id}
        )
        self.assertEqual(response.data['messages'][0]['id'], self.question.question_id)
        self.assertEqual(response.data['messages'][1]['id'], self.answer.answer_id)
