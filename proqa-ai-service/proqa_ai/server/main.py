import logging
from contextlib import asynccontextmanager
from threading import Thread

import uvicorn
from fastapi import FastAPI

from proqa_ai.controllers.text import buffer, generate_text_worker
from proqa_ai.routers.embedding import router as embedding_router
from proqa_ai.routers.text import router as text_router
from proqa_ai.routers.tokenize import router as tokenize_router
from proqa_ai.server.config import settings

__version__ = "1.0.0"


def create_app():
    """
    Factory function for creating FastAPI app.
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        thread = Thread(target=generate_text_worker)
        thread.start()
        yield
        # Stop the worker
        buffer.put(None)
        thread.join()

    app = FastAPI(title="proqa-ai-service", version=__version__, lifespan=lifespan)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     [%(name)s - %(asctime)s] %(message)s",
    )

    @app.get("/")
    def home():
        return {"message": "Welcome to proqa-ai-service.", "version": __version__}

    app.include_router(text_router)
    app.include_router(embedding_router)
    app.include_router(tokenize_router)
    return app


if __name__ == "__main__":
    _app = create_app()

    uvicorn.run(_app, host=settings.server_host, port=settings.server_port)
