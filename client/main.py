import sys
import json
import pygame
import asyncio
import websockets
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_1_X,
    PLAYER_2_X,
    PLAYER_DEFAULT_Y,
    UP,
    DOWN,
    NOTHING,
    BALL_RADIUS,
    BLACK, WHITE, RED
)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_paddle(x,y):
    pygame.draw.rect(
        screen, WHITE, pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    )

def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)


def render(player1_y, player2_y, ball_x, ball_y):
    # Render new state
    screen.fill(BLACK)
    draw_paddle(PLAYER_1_X, player1_y)
    draw_paddle(PLAYER_2_X, player2_y)
    draw_ball(ball_x, ball_y)
    pygame.display.flip()


async def send_player_input(websocket):
    while True:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move = UP
        elif keys[pygame.K_s]:
            move = DOWN
        else:
            move = NOTHING

        data = {"move": move}
        await websocket.send(json.dumps(data))

        # Limit the frame rate
        await asyncio.sleep(1 / FPS)


async def receive_game_state(websocket):
    while True:
        # Receive game state
        game_state = await websocket.recv()
        game_data = eval(json.loads(game_state))
        ball_x = game_data.get("ball_x")
        ball_y = game_data.get("ball_y")
        player1_y = game_data.get("player_1", PLAYER_DEFAULT_Y)
        player2_y = game_data.get("player_2", PLAYER_DEFAULT_Y)
        # Render
        render(player1_y, player2_y, ball_x, ball_y)


async def main():
    uri = "ws://localhost:8765/pong"

    async with websockets.connect(uri) as websocket:
        send_task = asyncio.create_task(send_player_input(websocket))
        receive_task = asyncio.create_task(receive_game_state(websocket))

        # Both tasks concurrently
        await asyncio.gather(send_task, receive_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
