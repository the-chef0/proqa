"""
Test cases for api/utils/chat_session.py
"""
from django.test import TestCase
from django.contrib.auth.models import User
from api.models import(
    ChatSession,
    Question,
    Answer,
    Collection,
    Source,
    Chunk
)
from api.utils.chat_session import (
    create_chat_session,
    delete_chat_session,
    set_chat_visibility,
    set_chat_pinning,
    get_chat_sessions,
    rate_answer,
    get_messages,
    get_raw_messages,
    add_message,
)
from tests.api.resources import constants as c


class TestChatSessionTool(TestCase):
    """Test cases for chat session tools."""

    def setUp(self):
        """
        Setup reusable elements for tests.
        """
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.session = ChatSession.objects.create(author=self.user1, title="test")

        self.collection = Collection.objects.create(name="testcollection", file_path="a/b/c")
        self.source = Source.objects.create(collection=self.collection,
                                                file_name="zucc.pdf",
                                                file_type = 'pdf')
        self.chunk = Chunk.objects.create(source=self.source, content="Version 4.2.0")
        self.session_id = self.session.session_id

    def test_session_creation(self):
        """
        Tests that a chat session is created correctly.
        """
        chat = create_chat_session(self.user1, "testtitle", "rgb(0,0,0)")
        self.assertEqual(ChatSession.objects.filter(session_id=chat).count(), 1)

    def test_session_deletion(self):
        """
        Tests that a chat session is deleted correctly and can only be deleted by creation 
            user.
        """
        result = delete_chat_session(user=self.user2, chat_session_id=self.session_id)
        self.assertFalse(result)
        self.assertEqual(ChatSession.objects.filter(session_id=self.session_id).count(), 1)

        result = delete_chat_session(user=self.user1, chat_session_id=self.session_id)
        self.assertTrue(result)
        self.assertEqual(ChatSession.objects.filter(session_id=self.session_id).count(), 0)

    def test_set_chat_visibillity(self):
        """
        Tests hiding and unhiding chat sessions and can only be done by creation user.
        """
        self.assertFalse(self.session.hidden)

        result = set_chat_visibility(self.user2, chat_session_id=self.session_id, hide=True)
        self.assertFalse(result)
        self.assertFalse(ChatSession.objects.get(session_id=self.session_id).hidden)

        result = set_chat_visibility(self.user1, chat_session_id=self.session_id, hide=True)
        self.assertTrue(result)
        self.assertTrue(ChatSession.objects.get(session_id=self.session_id).hidden)

        result = set_chat_visibility(self.user1, chat_session_id=self.session_id, hide=False)
        self.assertFalse(result)
        self.assertFalse(ChatSession.objects.get(session_id=self.session_id).hidden)

    def test_set_chat_pinning(self):
        """
        Tests pinning and unpinning chat sessions and can only be done by creation user.
        """
        self.assertFalse(self.session.pinned)

        result = set_chat_pinning(self.user2, chat_session_id=self.session_id, pin=True)
        self.assertFalse(result)
        self.assertFalse(ChatSession.objects.get(session_id=self.session_id).pinned)

        result = set_chat_pinning(self.user1, chat_session_id=self.session_id, pin=True)
        self.assertTrue(result)
        self.assertTrue(ChatSession.objects.get(session_id=self.session_id).pinned)

        result = set_chat_pinning(self.user1, chat_session_id=self.session_id, pin=False)
        self.assertFalse(result)
        self.assertFalse(ChatSession.objects.get(session_id=self.session_id).pinned)

    def test_get_chat_sessions(self):
        """
        Tests obtaining chats for a user.
        """
        sessions = get_chat_sessions(self.user1)
        self.assertEqual(len(sessions), 1)

        new_session = ChatSession.objects.create(author=self.user1, title="test2")
        new_session.save()
        sessions = get_chat_sessions(self.user1)

        self.assertEqual(len(sessions), 2)

    def test_get_raw_messages(self):
        """
        Tests obtaining raw messages of a chat session.
        """

        question = Question.objects.create(summary="summary",
                                                session=self.session,
                                                content="Mark Zuckerberg firmware version?")
        answer = Answer.objects.create(question=question,
                                            session=self.session,
                                            content="Firmware version 4.2.0",
                                            context=self.chunk)

        question.save()
        answer.save()
        messages = get_raw_messages(self.session_id)
        self.assertEqual(len(messages), 2)

        new_question = Question.objects.create(summary="summary2",
                                                session=self.session,
                                                content="Bill Gates")
        new_answer = Answer.objects.create(question=new_question,
                                            session=self.session,
                                            content="Wonk bookish nerd",
                                            context=self.chunk)
        new_question.save()
        new_answer.save()
        messages = get_raw_messages(self.session_id)

        self.assertEqual(len(messages), 4)

        self.assertEqual(messages[0]['is_answer'], False)
        self.assertEqual(messages[1]['is_answer'], True)
        self.assertEqual(messages[0]['content'], "Mark Zuckerberg firmware version?")
        self.assertEqual(messages[1]['content'], "Firmware version 4.2.0")
        self.assertEqual(messages[0]['context'], "Version 4.2.0")
        self.assertEqual('context' in messages[1], False)

        self.assertEqual(messages[2]['is_answer'], False)
        self.assertEqual(messages[3]['is_answer'], True)
        self.assertEqual(messages[2]['content'], "Bill Gates")
        self.assertEqual(messages[3]['content'], "Wonk bookish nerd")

    def test_rate_answer(self):
        """
        Tests rating an answer.
        """
        question = Question.objects.create(
            session=self.session,
            content=c.TEST_QUESTION
        )
        answer = Answer.objects.create(
            question=question,
            session=self.session
        )
        rating = rate_answer(answer_id=answer.answer_id, rating=1)
        self.assertEqual(rating, 1)

    def test_get_messages(self):
        """
        Tests getting messages.
        """
        question = Question.objects.create(
            session=self.session,
            content=c.TEST_QUESTION
        )
        answer = Answer.objects.create(
            question=question,
            session=self.session
        )
        messages = get_messages(chat_session_id=self.session.session_id)
        self.assertEqual(messages[0]['id'], question.question_id)
        self.assertEqual(messages[1]['id'], answer.answer_id)

    def test_add_message(self):
        """
        Tests adding a message to a chat session.
        """
        # Add question message
        message_count = len(self.session.question_set.all()) + len(self.session.answer_set.all())
        faq_question_id = add_message(self.user1, self.session_id, "test question", False, None)

        # Convert to list and get last message
        messages = list(self.session.question_set.all()) + list(self.session.answer_set.all())
        last_message = messages[-1]

        # Check that message was added
        self.assertEqual(len(messages), message_count + 1)
        self.assertEqual(last_message.question_id, faq_question_id)
        self.assertEqual(last_message.content, "test question")

        # Add answer message
        faq_answer_id = add_message(
            self.user1,
            self.session_id,
            "test answer",
            True,
            faq_question_id
        )

        # Convert to list and get last message
        messages = list(self.session.question_set.all()) + list(self.session.answer_set.all())
        last_message = messages[-1]

        # Check that message was added
        self.assertEqual(len(messages), message_count + 2)
        self.assertEqual(last_message.answer_id, faq_answer_id)
        self.assertEqual(last_message.content, "test answer")
        self.assertEqual(last_message.question, messages[-2])
