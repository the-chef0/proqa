import uuid

from django.contrib.auth.models import User
from django.db import models

from api.models.abstract import Rateable
from api.models.collection import Chunk
from api.models.model import LLM, PromptTemplate

class ChatSession(Rateable):
    """
    A chat session is a set of question answer pairs.
    """
    session_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(default="New Chat Session", max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    color = models.CharField(max_length=16, default="rgb(1,103,177)")

    def get_upvotes(self):
        """
        Get total number of upvotes from all answers in session.
        """
        if self.answer_set.exists():
            return self.answer_set.filter(rating=1).count()
        return 0

    def get_downvotes(self):
        """
        Get total number of downvotes from all answers in session.
        """
        if self.answer_set.exists():
            return self.answer_set.filter(rating=-1).count()
        return 0

    def __str__(self):
        return f'{self.title}'

class Question(models.Model):
    """
    Questions asked by users.
    """
    question_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content}'

class Answer(models.Model):
    """
    Answers to a given question.
    """
    answer_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    context = models.ForeignKey(Chunk, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(LLM, on_delete=models.SET_NULL, null=True)
    template = models.ForeignKey(
        PromptTemplate, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    is_flagged = models.BooleanField(default=False)
    moderation_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question.content}"

class FAQEntry(models.Model):
    """
    Frequently asked questions.
    """
    faq_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Question: {self.question} Answer: {self.answer}"

    class Meta:
        verbose_name_plural = "FAQ Entries"
