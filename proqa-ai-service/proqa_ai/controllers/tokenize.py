from sentencepiece import SentencePieceProcessor
from proqa_ai.server.config import settings

def _create_tokenizer_model(model_file: str) -> SentencePieceProcessor:
    """
    Create tokenizer model.

    Args:
        model_file (str): Model file.
    Returns:
        SentencePieceProcessor: Tokenizer model.
    """
    return SentencePieceProcessor(model_file=model_file)


def generate_tokens(text: str) -> list:
    """
    Generate tokens.

    Args:
        text (str): Text to generate tokens.
    Returns:
        list: Tokens.
    """
    tokenizer = _create_tokenizer_model(model_file=f"{settings.model_path}/llama.model")
    return tokenizer.encode(text)
