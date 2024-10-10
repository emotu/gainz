from fastapi import APIRouter, HTTPException, Depends
from openai import OpenAI, NotFoundError
from openai.types.beta import Assistant
from pydantic import BaseModel
from starlette import status

from app.services.auth import get_authenticated_user

router = APIRouter(prefix="/assistants", tags=["assistants"], dependencies=[Depends(get_authenticated_user)])
client = OpenAI()


class AssistantForm(BaseModel):
    name: str
    description: str | None
    instructions: str
    tools: list[dict] | None = None
    model: str | None = "gpt-4o-mini"


@router.get("/", response_model=list[Assistant])
async def query():
    """
    Allows a user to fetch their list of assistants. This will not be streamed directly from OpenAI,
    but queried from the database.
    """
    assistants = client.beta.assistants.list()

    return assistants


@router.get("/{assistant_id}", response_model=Assistant)
async def retrieve(assistant_id: str):
    """
    Retrieve an assistant from the API
    """

    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        return assistant
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assistant not found")


@router.post("/", response_model=Assistant)
async def create(payload: AssistantForm):
    assistant = client.beta.assistants.create(name=payload.name, description=payload.description,
                                              instructions=payload.instructions,
                                              model=payload.model, tools=payload.tools)

    return assistant


@router.patch("/{assistant_id}", response_model=Assistant)
async def create(assistant_id: str, payload: AssistantForm):
    try:
        assistant = client.beta.assistants.update(assistant_id, name=payload.name, description=payload.description,
                                                  instructions=payload.instructions,
                                                  model=payload.model, tools=payload.tools)
        return assistant
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assistant not found")


@router.delete("/{assistant_id}")
async def delete(assistant_id: str):
    try:
        response = client.beta.assistants.delete(assistant_id)
        return response
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assistant not found")
