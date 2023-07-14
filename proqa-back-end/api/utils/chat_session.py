"""
Helper functions for making API calls to Django backend.
"""
import uuid
from django.contrib.auth.models import User
from api.models import ChatSession, Question, Answer

# Create chat session
def create_chat_session(user: User, title: str, color: str) -> uuid.uuid4:
    """
    Creates chat session.

        Args:
            user (User): User object of author of chat session
            title (str): Title of chat session
        Returns:
            uuid: ID of created chat session
    """

    # Truncate title to 100 characters
    if len(title) > 100:
        title = title[:100]

    # Create chat session
    chat_session = ChatSession(title=title, author=user, color=color)
    chat_session.save()

    # Return ID of created chat session
    return chat_session.session_id

def __decrement_chunk_references(chat_session: ChatSession):
    """
    Decrements times_referenced for each chunk in chat_session

        Args:
            chat_session (ChatSession): Chat session to decrement in 
    """
    answers_in_session = chat_session.answer_set.all()
    for answer in answers_in_session:
        if answer.context is not None:
            used_chunk = answer.context
            used_chunk.times_referenced -= 1
            used_chunk.save()

# Delete chat session
def delete_chat_session(user: User, chat_session_id: uuid) -> bool:
    """
    Deletes chat session.

        Args:
            user (User): User object
            chat_session_id (uuid): ID of chat session
        Returns:
            bool: True if chat session is deleted, False if not
    """
    # Get chat session
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Check if user is author of chat session
    if chat_session.author != user:
        return False

    # Decrement references to chunks
    __decrement_chunk_references(chat_session)

    # Delete chat session
    chat_session.delete()

    # Return if chat session is deleted or not
    return not ChatSession.objects.filter(session_id=chat_session_id).exists()


# Set chat session visibility
def set_chat_visibility(user: User, chat_session_id: uuid, hide: bool) -> bool:
    """
    Sets chat session visibility.

        Args:
            user (User): User object
            chat_session_id (uuid): ID of chat session
            hide (bool): Hide chat session if True, show if False
        Returns:
            bool: True if chat session is visible, False if hidden
    """
    # Get chat session
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Check if user is author of chat session
    if chat_session.author != user:
        return False

    # Set chat session visibility
    chat_session.hidden = hide

    # If chat session is hidden, set pinned status to False
    if hide:
        chat_session.pinned = False

    chat_session.save()

    # Return if chat session is visible or not
    return ChatSession.objects.get(pk=chat_session.pk).hidden


# Set chat session pinned status
def set_chat_pinning(user: User, chat_session_id: uuid, pin: bool) -> bool:
    """
    Sets chat session pinned status.

        Args:
            user (User): User object
            chat_session_id (uuid): ID of chat session
            pin (bool): Pin chat session if True, unpin if False
        Returns:
            bool: True if chat session is pinned, False if not
    """
    # Get chat session
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Check if user is author of chat session
    if chat_session.author != user:
        return False

    # Set chat session pinned status
    chat_session.pinned = pin

    # If chat session is pinned, set hidden status to False
    if pin:
        chat_session.hidden = False

    chat_session.save()

    # Return if chat session is pinned or not
    return ChatSession.objects.get(pk=chat_session.pk).pinned


# Get chat sessions of a user
def get_chat_sessions(user: User) -> list:
    """
    Gets chat IDs, titles, hidden and pinned statuses, and colors of chat sessions of a user.

        Args:
            user (User): User object
        Returns:
            list: list of objects, containing chat session id, title, and hidden status
    """
    return list(ChatSession.objects.filter(author=user)
                                   .order_by('-created_at')
                                   .values('session_id', 'title', 'hidden', 'pinned', 'color'))


# Rate answer
def rate_answer(answer_id: uuid, rating: int) -> bool:
    """
    Rates answer.

        Args:
            answer_id (uuid): ID of answer
            rating (int): Rating of answer
        Returns:
            bool: True if rating is successful, False if not
    """
    # Get answer
    answer = Answer.objects.get(answer_id=answer_id)

    # Set answer rating
    answer.rating = rating
    answer.save()

    # Return if rating is successful or not
    return Answer.objects.get(pk=answer.pk).rating


# Get chat session messages
def get_messages(chat_session_id: uuid) -> list:
    """
    Gets the chat messages of a given chat session.

        Args:
            chat_session_id (uuid): ID of chat session
        Returns:
            list: list of messages sorted by creation time
    """
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Get all answers and questions of chat session
    answers = list(chat_session.answer_set.all())
    questions = list(chat_session.question_set.all())

    # JSON version containing ID, is_answer, content, rating, notes for every answer
    answer_list_json = []

    for answer in answers:
        source = None

        if answer.context is not None:
            if answer.context.source is not None:
                source = {
                    "filepath": answer.context.source.collection.file_path,
                    "title": answer.context.source.file_name,
                    "context": answer.context.content
                }
            else:
                source = {
                    "filepath": None,
                    "title": "Document has been modified or removed",
                    "context": answer.context.content
                }

        answer_json = {
            "id": answer.answer_id,
            "created_at": answer.created_at,
            "is_answer": True,
            "content": answer.content,
            "rating": answer.rating,
            "source": source,
        }
        answer_list_json.append(answer_json)

    # JSON version containing ID, content, source, context for every question
    question_list_json = []

    for question in questions:
        question_json = {
            "id": question.question_id,
            "created_at": question.created_at,
            "is_answer": False,
            "content": question.content,
        }
        question_list_json.append(question_json)

    messages = question_list_json + answer_list_json

    # Sort messages by created_at
    messages.sort(key=lambda message: message["created_at"])

    return messages

def get_raw_messages(chat_session_id: uuid) -> list:
    """
    Internal function for getting the chat messages given a chat session id.

        Args:
            chat_session_id (uuid): ID of chat session
        Returns:
            list: list of messages sorted by creation time
    """
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Get all answers and questions of chat session
    answers = list(chat_session.answer_set.all())

    messages = []
    for answer in answers:
        question = answer.question

        # Check if context is not None
        if answer.context is not None:
            messages.append({
                "is_answer": False,
                "content": question.content,
                "context": answer.context.content,
                "created_at": question.created_at
            })
        else:
            messages.append({
                "is_answer": False,
                "content": question.content,
                "context": None,
                "created_at": question.created_at
            })

        messages.append({
            "is_answer": True,
            "content": answer.content,
            "created_at": answer.created_at
        })

    # Sort messages by created_at
    messages.sort(key=lambda message: message["created_at"])

    return messages

def add_message(
        user: User,
        chat_session_id: uuid,
        content: str,
        is_answer: bool,
        question_id: uuid
        ) -> uuid:
    """
    Adds message to chat session.

        Args:
            user (User): User object
            chat_session_id (uuid): ID of chat session
            content (str): Content of message
            is_answer (bool): True if message is answer, False if not
            question_id (uuid): ID of question if message is answer, None if not
        Returns:
            uuid: ID of message if message is added, None if not
    """
    # Get chat session
    chat_session = ChatSession.objects.get(session_id=chat_session_id)

    # Check if user is author of chat session
    if chat_session.author != user:
        return None

    # Check if message is answer or question
    if is_answer:
        # Create answer
        answer = Answer()

        # Set answer content
        answer.content = content
        answer.question = Question.objects.get(question_id=question_id)
        answer.session = chat_session
        answer.save()

        # Return uuid of answer
        return Answer.objects.get(pk=answer.pk).answer_id

    # If message is question
    # Create question
    question = Question()

    # Set question content
    question.content = content
    question.session = chat_session
    question.save()

    # Return uuid of question
    return Question.objects.get(pk=question.pk).question_id
