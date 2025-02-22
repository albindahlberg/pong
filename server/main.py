from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection import ConnectionManager
from game_logic import Game
from config import NOTHING, NUM_PLAYERS

app = FastAPI()
manager = ConnectionManager()
game = Game()


@app.websocket("/pong")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    player_id = len(manager.active_connections)

    if len(manager.active_connections) == NUM_PLAYERS:
        game.start()

    try:
        while True:
            data = await websocket.receive_json()
            # Default to NOTHING if missing
            move = data.get("move", NOTHING)
            # Update game state based on player input
            game.update_state(player_id, move)
            state = game.get_state()
            await manager.broadcast(state)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        game.reset()
