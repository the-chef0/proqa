from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingRequest:
    """
    Schema for generate embeddings request.
    """

    text: str
    passage: bool = True


@dataclass(frozen=True)
class EmbeddingResponse:
    """
    Schema for generate embeddings response.
    """

    text: str
    embedding: list
