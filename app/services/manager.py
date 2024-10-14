from starlette.websockets import WebSocket


class WebSocketManager:

    def __init__(self):
        """ WebSocket connection manager """
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        client_connections = self._connections.get(client_id, [])
        if websocket not in client_connections:
            client_connections.append(websocket)

        self._connections[client_id] = client_connections

    async def disconnect(self, client_id: str, websocket: WebSocket):
        client_connections = self._connections.get(client_id, [])
        if websocket in client_connections:
            client_connections.remove(websocket)

        self._connections[client_id] = client_connections

    def get_connection(self, client_id: str) -> WebSocket | None:
        return self._connections.get(client_id, None)

    async def broadcast_message(self, client_id: str, action: str, message: str, role: str, sender: str) -> bool:
        client_connections = self._connections.get(client_id, [])
        for websocket in client_connections:
            await websocket.send_json(dict(action=action, message=message, role=role, sender=sender))
        return True


manager = WebSocketManager()
