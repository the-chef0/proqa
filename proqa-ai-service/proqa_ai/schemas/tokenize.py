from dataclasses import dataclass


@dataclass(frozen=True)
class TokenizeRequest:
    """
    Schema for generate token request.
    """

    text: str


@dataclass(frozen=True)
class TokenizeResponse:
    """
    Schema for generate token response.
    """

    text: str
    tokens: list
    num_tokens: int
