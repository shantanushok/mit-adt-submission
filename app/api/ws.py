from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # We make a copy of the list to iterate to avoid modification issues during iteration
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to a websocket client: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We just block waiting for messages (we don't necessarily process them)
            # This keeps the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
