import uuid
from threading import Lock

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from strands import Agent

from bedrock_client import build_agent

app = FastAPI(title="Chat with Bedrock API")

_sessions: dict[str, Agent] = {}
_sessions_lock = Lock()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str


def _get_agent(session_id: str) -> Agent:
    with _sessions_lock:
        agent = _sessions.get(session_id)
        if agent is None:
            agent = build_agent()
            _sessions[session_id] = agent
        return agent


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")

    session_id = request.session_id or str(uuid.uuid4())
    agent = _get_agent(session_id)

    try:
        response = agent(request.message)
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(status_code=502, detail=f"Bedrock request failed: {exc}")

    return ChatResponse(session_id=session_id, reply=str(response))


@app.delete("/chat/{session_id}")
def reset_session(session_id: str) -> dict:
    with _sessions_lock:
        _sessions.pop(session_id, None)
    return {"session_id": session_id, "reset": True}
