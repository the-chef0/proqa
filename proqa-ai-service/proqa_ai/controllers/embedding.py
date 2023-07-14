import torch
import torch.nn.functional as F
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoModel, AutoTokenizer
from proqa_ai.server.config import settings

def _generate_embedding_hugging_face(text: str, passage: bool, model_name: str = "all-MiniLM-L6-v2") -> list:
    """
    Generate embedding from the HuggingFaceEmbeddings library.
    Only supports sentence-transformers models.

    Args:
        text (str): Text to generate embedding.
        passage (bool): If given text is a passage or not.
    Returns:
        list: Embedding.
    """
    transformer = HuggingFaceEmbeddings(model_name=model_name, cache_folder=settings.model_path)
    embeddings = transformer.embed_query(text)
    return embeddings


def _generate_embedding_transformers(text: str, passage: bool, model_name: str = "intfloat/e5-large-v2") -> list:
    def average_pool(last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
    
    input_text = [f"{'passage' if passage else 'query'}: {text}"]
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=settings.model_path)
    model = AutoModel.from_pretrained(model_name, cache_dir=settings.model_path)

    batch_dict = tokenizer(input_text, max_length=512, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict["attention_mask"])
    return F.normalize(embeddings, p=2, dim=1).tolist()[0]


def generate_embedding(text: str, passage: bool, model_name: str = "all-MiniLM-L6-v2") -> list:
    """
    Generate embedding.

    Args:
        text (str): Text to generate embedding.
    Returns:
        list: Embedding.
    """    
    if model_name == "all-MiniLM-L6-v2":
        return _generate_embedding_hugging_face(text, passage, model_name=model_name)
    elif model_name == "intfloat/e5-large-v2":
        return _generate_embedding_transformers(text, passage, model_name=model_name)
    else:
        raise ValueError("Invalid model name.")
