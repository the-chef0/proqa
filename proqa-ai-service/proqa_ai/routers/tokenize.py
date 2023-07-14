from fastapi import APIRouter

from proqa_ai.controllers.tokenize import generate_tokens
from proqa_ai.schemas.tokenize import TokenizeRequest, TokenizeResponse

router = APIRouter()


@router.post("/tokenize", response_model=TokenizeResponse)
def tokenize(request: TokenizeRequest):
    """
    Generate tokens from text.

    Args:
        request (TokenizeRequest): Tokenize
    Returns:
        TokenizeResponse: Tokenize response.
    """

    tokens = generate_tokens(request.text)

    return TokenizeResponse(
        text=request.text,
        tokens=tokens,
        num_tokens=len(tokens)
    )