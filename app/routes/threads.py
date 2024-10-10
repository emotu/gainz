from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from openai import OpenAI, NotFoundError
from openai.types.beta import Thread
from openai.types.beta.threads import Run
from pydantic import BaseModel
from starlette import status

from app.models import User
from app.services.auth import get_authenticated_user, get_current_user
from app.services.runs import stream_assistant_runs

router = APIRouter(prefix="/threads", tags=["threads"], dependencies=[Depends(get_authenticated_user)])
client = OpenAI()


class MessageForm(BaseModel):
    content: str


class RunAssistantForm(BaseModel):
    assistant_id: str


@router.get("/{thread_id}", response_model=Thread)
async def retrieve(thread_id: str):
    """
    Retrieve an assistant from the API
    """

    try:
        thread = client.beta.threads.retrieve(thread_id)
        return thread
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")


@router.post("/", response_model=Thread)
async def create(payload: MessageForm):
    thread = client.beta.threads.create(messages=[dict(role="user", content=payload.content)])
    return thread


@router.post("/{thread_id}/messages")
async def message(thread_id: str, payload: MessageForm):
    try:
        thread = client.beta.threads.retrieve(thread_id)
        _message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=payload.content)
        return _message
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assistant not found")


@router.get("/{thread_id}/messages")
async def retrieve(thread_id: str):
    """
    Retrieve an assistant from the API
    """

    try:
        messages = client.beta.threads.messages.list(thread_id, limit=50)
        return messages
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")


@router.delete("/{thread_id}")
async def delete(thread_id: str):
    try:
        response = client.beta.threads.delete(thread_id)
        return response
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")


@router.get("/{thread_id}/runs")
async def list_runs(thread_id: str):
    try:
        run = client.beta.threads.runs.list(thread_id=thread_id, limit=50)
        return run
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")


@router.get("/{thread_id}/runs/{run_id}", response_model=Run)
async def retrieve_run(thread_id: str, run_id: str):
    try:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")


@router.post("/{thread_id}/run")
async def run_thread(thread_id: str, payload: RunAssistantForm,
                     current_user: Annotated[User, Depends(get_current_user)],
                     background_tasks: BackgroundTasks):
    try:
        thread = client.beta.threads.retrieve(thread_id)
        assistant = client.beta.assistants.retrieve(payload.assistant_id)
        background_tasks.add_task(stream_assistant_runs, assistant=assistant, client_id=str(current_user.id),
                                  thread_id=thread.id, assistant_id=assistant.id)

        return dict(status="ok")

    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assistant not found")
