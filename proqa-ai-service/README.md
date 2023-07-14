# proqa-ai-service

> ⚠️ Read [`CONTRIBUTING.md`](CONTRIBUTING.md) to setup the environment and understand the development workflow.

## Usage
The AI text service can be started locally by executing the following command:
```shell
uvicorn --factory proqa_ai.server:create_text_app --host localhost --port 8001
```
A more comprehensive documentation can be found at the `HOST:PORT/docs` endpoint, for example, http://localhost:8001/docs for a local environment.

The below endpoints are supported by the AI service. These can be tested by running the following commands. Please ensure that the model weights are present in the `proqa_ai/weights` directory at renamed to `<model_name>-<size>.bin`, eg: `vicuna-7b.bin`. The weights can be downloaded at the following links:
1. [vicuna-7b](https://huggingface.co/TheBloke/vicuna-7B-v1.3-GGML/blob/main/vicuna-7b-v1.3.ggmlv3.q5_K_S.bin)
2. [vicuna-13b](https://huggingface.co/TheBloke/vicuna-13b-v1.3-GGML/blob/main/vicuna-13b-v1.3.ggmlv3.q5_K_S.bin)

### `/text`
```shell
curl -X 'POST' \
  'http://localhost:8001/text' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_id": "vicuna-7b",
  "prompt": "What is the difference between alpacas and vicunas?"
}'
```

### `/embedding`
```shell
curl -X 'POST' \
  'http://localhost:8001/embedding' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "What is the difference between alpacas and vicunas?"
}'
```