"""
Endpoints that are used to communicate with Postgres (chat sessions).
"""
import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.utils.chat_session import (
    create_chat_session,
    delete_chat_session,
    set_chat_visibility,
    set_chat_pinning,
    get_chat_sessions,
    rate_answer,
    get_messages,
    add_message
)


@api_view(['POST'])
def creation(request) -> Response:
    """
    Endpoint for creating a chat session.

        Args:
            request (Request): API request, with chat session title and color
        Returns:
            Response: ID of created chat session, as a string
    """
    # Get user and title from request
    user = request.user
    title = request.data["title"]
    color = request.data["color"]

    # Create chat session
    chat_session_id = create_chat_session(user=user, title=title, color=color)

    # Return ID of created chat session
    return Response({"id": chat_session_id})


@api_view(['POST'])
def deletion(request) -> Response:
    """
    Endpoint for deleting a chat session.

        Args:
            request (Request): API request with chat session id
        Returns:
            Response: "deleted" if chat session was deleted, "not delete" otherwise
    """
    # Get chat session id and user from request
    user = request.user
    chat_session_id = request.data['chat_session_id']

    # Convert string of uuid to UUID object
    chat_session_uuid = uuid.UUID(chat_session_id)

    # Delete chat session
    chat_deleted = delete_chat_session(user, chat_session_uuid)

    # Return if chat session is deleted or not
    return Response({"status": "deleted"}) if chat_deleted else Response({"status": "not deleted"})


@api_view(['POST'])
def hiding(request) -> Response:
    """
    Endpoint for (un)hiding a chat session.

        Args:
            request (Request): API request with chat session id and hide value
        Returns:
            Response: "hidden" if chat session was hidden
            Response: "shown" if chat session was unhidden
    """
    # Get chat session id and user from request
    user = request.user
    chat_session_id = request.data['chat_session_id']

    # Convert string of uuid to UUID object
    chat_session_uuid = uuid.UUID(chat_session_id)

    # Get hide value from request
    hide = request.data['hide']

    # Hide chat session
    chat_hidden = set_chat_visibility(user, chat_session_uuid, hide)

    # Return if chat session is hidden or not
    return Response({"status": "hidden"}) if chat_hidden else Response({"status": "shown"})


@api_view(['POST'])
def pinning(request) -> Response:
    """
    Endpoint for (un)pinning a chat session.

        Args:
            request (Request): API request with chat session id and pin value
        Returns:
            Response: "pinned" if chat session was pinned
            Response: "unpinned" if chat session was unpinned
    """
    # Get chat session id and user from request
    user = request.user
    chat_session_id = request.data['chat_session_id']

    # Convert string of uuid to UUID object
    chat_session_uuid = uuid.UUID(chat_session_id)

    # Get pin value from request
    pin = request.data['pin']

    # Pin chat session
    chat_pinned = set_chat_pinning(user, chat_session_uuid, pin)

    # Return if chat session is pinned or not
    return Response({"status": "pinned"}) if chat_pinned else Response({"status": "unpinned"})


@api_view(['POST'])
def rating(request) -> Response:
    """
    Endpoint for rating an answer.

        Args:
            request (Request): API request with chat session id, answer id and rating
        Returns:
            Response: "rated" if answer was rated
            Response: "not rated" if answer was not rated
    """
    answer_id = request.data['answer_id']
    answer_rating = request.data['rating']

    # Convert string of uuid to UUID object
    answer_uuid = uuid.UUID(answer_id)

    # Rate answer
    answer_rated = rate_answer(answer_uuid, answer_rating)

    # Return if answer is rated or not
    return Response({"status": "rated"}) if answer_rated else Response({"status": "not rated"})


@api_view(['POST'])
def history(request) -> Response:
    """
    Endpoint for returning all chat sessions of a user.

        Args:
            request (Request): API request with user id
        Returns:
            Response: a list of chat session ids, titles, hidden and pinned statuses, and colors
    """
    user = request.user
    chat_session_ids = get_chat_sessions(user=user)
    return Response({"chats": chat_session_ids})


@api_view(['POST'])
def messages(request) -> Response:
    """
    Endpoint for returning all chat data of an already existing chat session.

        Args:
            request (Request): API request with chat session id
        Returns:
            Response: a list of objects, each containing: question, answer, context, source
    """
    chat_session_id = uuid.UUID(request.data['session'])
    chat_messages = get_messages(chat_session_id)

    # Return list of messages
    return Response({"messages": chat_messages})


@api_view(['POST'])
def saving(request) -> Response:
    """
    Endpoint for adding a message to an already existing chat session.

        Args:
            request (Request): API request with chat session id, message, and message type
        Returns:
            Response: uuid of created message
    """
    # Get user, chat session id, message, and message type from request
    user = request.user
    chat_session_id = uuid.UUID(request.data['session'])
    content = request.data["content"]
    is_answer = request.data["is_answer"]
    question_id = None

    if is_answer:
        question_id = uuid.UUID(request.data['question_id'])

    # Add message
    message_id = add_message(user, chat_session_id, content, is_answer, question_id)

    # Return if message is added or not
    return Response({"message_id": message_id})
