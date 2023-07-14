import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from proqa_ai.server import create_app
from tests import constants


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    return TestClient(create_app())


def test_app_status_code(app: TestClient):
    """
    Test app status code.
    """
    response = app.get("/")
    assert response.status_code == 200


def test_text_endpoint(app: TestClient):
    """
    Test text endpoint.
    """
    response = app.post(
        "/text",
        json={
            "prompt": constants.PROMPT,
            "model_settings": {"model_name": constants.MODEL_NAME},
            "message_id": constants.MESSAGE_ID,
            "streaming_settings": {
                "session_id": constants.SESSION_ID,
                "channel": constants.CHANNEL,
            }
        },
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["prompt"] == constants.PROMPT
    assert response_json["message_id"] == constants.MESSAGE_ID
    assert response_json["model_settings"]["model_name"] == constants.MODEL_NAME
    assert response_json["streaming_settings"]["session_id"] == constants.SESSION_ID
    assert response_json["streaming_settings"]["channel"] == constants.CHANNEL


def test_embedding_endpoint(mocker: MockerFixture, app: TestClient):
    """
    Test embedding endpoint.
    """
    mocker.patch(
        "proqa_ai.routers.embedding.generate_embedding",
        return_value=constants.GENERATED_EMBEDDING,
    )

    response = app.post("/embedding", json={"text": constants.TEXT})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["text"] == constants.TEXT
    assert response_json["embedding"] == constants.GENERATED_EMBEDDING


def test_tokenize_endpoint(mocker: MockerFixture, app: TestClient):
    """
    Test tokenize endpoint.
    """
    mocker.patch(
        "proqa_ai.routers.tokenize.generate_tokens",
        return_value=constants.GENERATED_TOKENS,
    )

    response = app.post("/tokenize", json={"text": constants.TEXT})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["text"] == constants.TEXT
    assert response_json["tokens"] == constants.GENERATED_TOKENS
    assert response_json["num_tokens"] == len(constants.GENERATED_TOKENS)
