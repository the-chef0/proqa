"""
Endpoints that are used to communicate with the LLM.
"""
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import ChatSession, Question, Answer, Chunk, LLM, PromptTemplate
from api.utils.aiservice import PromptBuilder
from api.utils.aiservice_text import TextAdapter
from api.utils.aiservice_embedding import EmbeddingAdapter
from api.utils.aiservice_tokenize import TokenizeAdapter
from api.utils.chat_session import get_raw_messages
from api.utils.context import get_context_uuid
from api.utils.vectordb import VECTORDB_CLIENT

embedding_adapter = EmbeddingAdapter()
text_adapter = TextAdapter()
tokenize_adapter = TokenizeAdapter()

@api_view(['POST'])
def question(request) -> Response:
    """
    Endpoint for asking a question to the AI service.

        Args:
            request (Request): API request
        Returns:
            Response: JSON of format {"context", "source", "answer_id"} if AI service is available
    """
    question_text = request.data['question']
    chat_session_id = uuid.UUID(request.data['session'])
    session = ChatSession.objects.get(session_id=chat_session_id)
    messages = get_raw_messages(chat_session_id)

    # save question to DB
    question_obj = Question(summary="summary",
                            session=session,
                            content=question_text)
    question_obj.save()

    # Get embedding of question
    question_embedding = embedding_adapter.batch_get(messages=messages, last_question=question_text)

    # Query vector DB with embedding of question
    chunk_id = get_context_uuid(VECTORDB_CLIENT, question_embedding)
    chunk = Chunk.objects.get(chunk_id=chunk_id)
    # Increment number of chunk references
    chunk.times_referenced += 1
    chunk.save()

    # get the active model
    model = LLM.objects.get(active=True)
    text_adapter.update_model(model=model)

    # Update the active prompt in the prompt builder and build prompt.
    prompt_template = PromptTemplate.objects.get(active=True)
    prompt_builder = PromptBuilder(prompt_template, tokenize_adapter.get, model.context_size)

    prompt = prompt_builder.get_prompt(
        messages, question_text, chunk.content
    )

    # save temporary answer object
    answer_obj = Answer(question=question_obj,
                        session=session, context=chunk, model=model)
    answer_obj.save()

    # Send prompt to AI service and get answer
    status_code = text_adapter.get(channel=request.user.username,
                                   prompt=prompt,
                                   session_id=str(chat_session_id),
                                   message_id=str(answer_obj.answer_id))

    # Raise exception in case the AI service is not available
    if status_code != 200:
        raise ConnectionError("AI service not available.")

    return Response({"context": chunk.content,
                     "source": chunk.source.file_name,
                     "question_id": question_obj.question_id,
                     "answer_id": answer_obj.answer_id})


@api_view(['POST'])
def answer(request) -> Response:
    """
    Endpoint for receiving the answer from the AI service.
    Strictly used for saving the answer to the DB.

        Args:
            request (Request): API request
        Returns:
            Response: Empty response
    """
    session_id = uuid.UUID(request.data["session_id"])
    answer_text = request.data["answer"]
    answer_obj = ChatSession.objects.get(
        session_id=session_id).answer_set.last()
    answer_obj.content = answer_text
    answer_obj.save()

    return Response()
