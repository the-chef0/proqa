from typing import Optional

from pydantic import BaseSettings


# As this class will never have public methods, we disable this pylint check
# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Class that defines the settings of the application
    """
    # Server settings
    server_host: str = "0.0.0.0"
    server_port: int = 8081

    # Pushpin related settings
    pushpin_http_url: str = "http://pushpin:5561"

    # Backend related settings
    backend_http_url: str = "http://django:8000"

    # Model related settings
    model_path: str = "./proqa_ai/weights"

    # Number of threads to use in LLM
    thread_count: Optional[int] = None

    # Text generation timeout
    text_generation_timeout: int = 900

settings = Settings()
