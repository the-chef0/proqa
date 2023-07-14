from fastapi import APIRouter

from proqa_ai.controllers.embedding import generate_embedding
from proqa_ai.schemas.embedding import EmbeddingRequest, EmbeddingResponse

router = APIRouter()


@router.post("/embedding", response_model=EmbeddingResponse)
def embedding(request: EmbeddingRequest):
    """
    Generate embedding from given text.

    Args:
        request (EmbeddingRequest): Request body.
    Returns:
        EmbeddingResponse: Response body./
    """
    generated_embedding = generate_embedding(request.text, request.passage)
    return EmbeddingResponse(text=request.text, embedding=generated_embedding)
