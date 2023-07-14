from langchain.llms import LlamaCpp

from proqa_ai.schemas.text import ModelSettings, StreamingSettings
from proqa_ai.server.config import settings
from proqa_ai.utilities.callback import StreamingCallbackHandler


class ModelManager:
    """
    Responsible for loading the model and performing inference.
    """
    def __init__(self, model_settings: ModelSettings = None):
        self.model_settings = model_settings
        self.model = None

    def _factory(self, model_settings: ModelSettings) -> LlamaCpp:
        """
        Factory method for loading the model.

        Args:
            model_settings (ModelSettings): Model settings.
        Returns:
            LlamaCpp: Loaded model.
        """
        if self.model is not None and self.model_settings == model_settings:
            return self.model

        self.model_settings = model_settings
        self.model = LlamaCpp(
            model_path=f"{settings.model_path}/{model_settings.model_name}.bin",
            n_ctx=model_settings.n_ctx,
            n_batch=model_settings.n_batch,
            n_threads=settings.thread_count,
            n_gpu_layers=model_settings.n_gpu_layers,
            temperature=model_settings.temperature,
            streaming=True
        )
        return self.model

    def generate_text(
        self, prompt: str, message_id: str, model_settings: ModelSettings,
        streaming_settings: StreamingSettings
    ) -> str:
        """
        Generate text from prompt.

        Args:
            prompt (str): Prompt.
            message_id (str): ID of the answer
            model_settings (ModelSettings): Model settings.
            streaming_settings (StreamingSettings): Streaming settings.
        Returns:
            str: Generated text.
        """
        llm = self._factory(model_settings)
        streaming_handler = StreamingCallbackHandler(
            streaming_settings.channel, streaming_settings.session_id, message_id
        )
        generated_text = llm(prompt, callbacks=[streaming_handler])

        return generated_text
