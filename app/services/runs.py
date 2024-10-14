from typing import override

from openai import AsyncOpenAI as OpenAI, NotFoundError
from openai.lib.streaming import AsyncAssistantEventHandler
from openai.types.beta import AssistantStreamEvent, Assistant
from openai.types.beta.threads import TextDelta, Text, Message

from app.models import User
from app.services.manager import WebSocketManager

client = OpenAI()


async def stream_assistant_runs(*, assistant_id: str, user_id: str, thread_id: str, manager: WebSocketManager):
    try:
        thread = await client.beta.threads.retrieve(thread_id)
        assistant = await client.beta.assistants.retrieve(assistant_id)
        async with client.beta.threads.runs.stream(thread_id=thread.id, assistant_id=assistant_id,
                                                   event_handler=EventHandler(client_id=thread.id,
                                                                              manager=manager,
                                                                              assistant=assistant)) as stream:
            await stream.until_done()

        return dict(status="OK")
    except NotFoundError:
        return None


async def post_user_message(thread_id: str, user: User, message: str, manager: WebSocketManager) -> Message | None:
    try:
        thread = client.beta.threads.retrieve(thread_id)
        _message = client.beta.threads.messages.create(thread_id=thread.id, role="user",
                                                       content=message, metadata=dict(user_id=user.id, name=user.name))

        await manager.broadcast_message(thread.id, action="start", message="", role="user", sender=user.name)

        return _message
    except NotFoundError:
        return None


class EventHandler(AsyncAssistantEventHandler):

    def __init__(self, *, client_id: str, manager: WebSocketManager, assistant: Assistant):
        super().__init__()
        self.client_id = client_id
        self.assistant = assistant
        self.manager = manager

    @override
    async def on_text_created(self, event: AssistantStreamEvent) -> None:
        print(f"\n{self.assistant.name} > ", end="", flush=True)
        await self.manager.broadcast_message(self.client_id, action="start", message="", role="assistant", sender=self.assistant.name)

    @override
    async def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        print(delta.value, end="", flush=True)
        await self.manager.broadcast_message(self.client_id, action="body", message=delta.value, role="assistant", sender=self.assistant.name)

    async def on_text_done(self, text: Text) -> None:
        print("\n--\n", end="", flush=True)
        await self.manager.broadcast_message(self.client_id, action="stop", message="--", role="assistant", sender=self.assistant.name)
