import json
from typing import List, Dict
from fastapi import WebSocket
from dataclasses import dataclass


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket, int] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, state: Dict):
        # Convert dictionary to JSON
        message = json.dumps(state)
        for connection in self.active_connections:
            await connection.send_text(message)
