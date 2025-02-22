import json
from typing import List, Dict
from fastapi import WebSocket


class ConnectionManager:
    """Manages websocket connections"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept up to two incoming websocket connections"""
        if len(self.active_connections) == 2:
            return

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Disconnect a connection"""
        self.active_connections.remove(websocket)

    async def broadcast(self, data: Dict):
        """Broadcast a message to all connections"""
        message = json.dumps(data)
        for connection in self.active_connections:
            await connection.send_text(message)
