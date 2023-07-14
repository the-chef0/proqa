from dataclasses import dataclass

from pydantic import BaseSettings


class ModelSettings(BaseSettings):
    """
    Class defining the settings of the LLM.
    """
    model_name: str
    n_ctx: int = 2048
    n_batch: int = 1024
    n_gpu_layers: int = 0
    temperature: float = 0.2


class StreamingSettings(BaseSettings):
    """
    Class defining the settings of the streaming.
    """
    channel: str
    session_id: str


@dataclass(frozen=True)
class TextRequest:
    """
    Schema for generate text request.
    """

    prompt: str
    message_id: str
    model_settings: ModelSettings
    streaming_settings: StreamingSettings


@dataclass(frozen=True)
class TextResponse:
    """
    Schema for generate text response.
    """

    prompt: str
    message_id: str
    streaming_settings: StreamingSettings
    model_settings: ModelSettings
