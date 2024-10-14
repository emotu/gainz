from typing import Annotated

from fastapi import APIRouter, Query, BackgroundTasks
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.services.auth import get_user_from_token
from app.services.manager import manager
from app.services.runs import post_user_message, stream_assistant_runs

router = APIRouter(prefix="/ws", tags=["websockets"])


@router.websocket("/{thread_id}")
async def client_socket(*, websocket: WebSocket, thread_id: str, token: Annotated[str, Query()],
                        background_tasks: BackgroundTasks):
    try:
        current_user = await get_user_from_token(token)
        user_id = str(current_user.id)
        await manager.connect(client_id=thread_id, websocket=websocket)

        while True:
            data: dict = await websocket.receive_json()
            action = data.get("action", "message")
            message: str | None = data.get("message", None)
            assistant_id: str | None = data.get("assistant_id", None)

            if action == "message" and message is not None:
                background_tasks.add_task(post_user_message, thread_id=thread_id, message=message)

            if action == "run" and assistant_id is not None:
                await stream_assistant_runs(thread_id=thread_id, user_id=user_id,
                                            assistant_id=assistant_id, manager=manager)
    except WebSocketDisconnect:
        print("Exception called")
        await manager.disconnect(client_id=thread_id, websocket=websocket)
