# Strands Bedrock Chat Agent

A minimal Python chat agent using `strands-agents` and Amazon Bedrock, available as a
CLI chat (`chat.py`) and a REST API (`restapi.py`).

## Prerequisites

- Python 3.10+
- Access to your selected Bedrock model in the target AWS Region
- Either a Bedrock API key, or standard AWS credentials (e.g. via `aws configure`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure model and credentials

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

`AWS_BEARER_TOKEN_BEDROCK` is a Bedrock API key generated from the Bedrock console
("API keys" section) — the simplest way to authenticate locally without configuring
a full AWS profile. Alternatively, leave it blank and set `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY` (also in `.env.example`) to use standard IAM credentials.

`.env` is loaded automatically by both `chat.py` and `restapi.py`.

## Run the CLI chat

```bash
python chat.py
```

Type `exit` or `quit` to end the chat.

## Run the REST API

```bash
uvicorn restapi:app --reload
```

Endpoints:

- `POST /chat` — body `{"message": "hello", "session_id": "optional"}`. Returns
  `{"session_id": "...", "reply": "..."}`. Reuse the returned `session_id` to keep
  conversation history across requests.
- `DELETE /chat/{session_id}` — clears a session's conversation history.
- `GET /health` — health check.

Example:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```
# chat-agent
