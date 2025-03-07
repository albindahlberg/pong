import json
import math
import random
from dataclasses import dataclass
from pygame import Vector2, Rect

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    PLAYER_1,
    PLAYER_2,
    PLAYER_1_X,
    PLAYER_2_X,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    BALL_RADIUS,
    BALL_SPEED,
)


@dataclass
class Player:
    x: int
    y: int


@dataclass
class Ball:
    angle = math.radians(random.randint(0, 360))    
    position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    velocity = BALL_SPEED * Vector2(math.cos(angle), math.sin(angle))


@dataclass
class GameState:
    """Class for full game state"""

    ball: Ball = Ball()
    player_1: Player = Player(x=PLAYER_1_X, y=SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2)
    player_2: Player = Player(x=PLAYER_2_X, y=SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2)

    def reset_ball(self):
        self.ball = Ball()


class Game:
    """Class for handling game logic"""

    def __init__(self):
        self.state = GameState()
        self.running = False

    def start(self):
        """Allows state to update"""
        self.running = True

    def reset(self):
        """Resets the game state"""
        self.state = GameState()
        self.running = False

    def get_state(self):
        """Yields the current state for clients (only what they should see)"""
        state = {
            "player_1": self.state.player_1.y,
            "player_2": self.state.player_2.y,
            "ball_x": self.state.ball.position.x,
            "ball_y": self.state.ball.position.y,
        }
        return json.dumps(state)

    def update_ball(self):
        """Update ball position"""
        ball = self.state.ball
        player_1 = self.state.player_1
        player_2 = self.state.player_2

        # Collision with top and bottom walls
        if (
            ball.position.y - BALL_RADIUS <= 0
            or ball.position.y + BALL_RADIUS >= SCREEN_HEIGHT
        ):
            ball.velocity.y = -ball.velocity.y

        # Ball hitbox for collisions
        ball_rect = Rect(
            ball.position.x - BALL_RADIUS,
            ball.position.y - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )

        # Collision with player 1
        player_1_rect = Rect(PLAYER_1_X, player_1.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        if player_1_rect.colliderect(ball_rect):
            ball.velocity.x = ball.velocity.x

        # Collision with player 2
        player_2_rect = Rect(
            PLAYER_2_X - PLAYER_WIDTH, player_2.y, PLAYER_WIDTH, PLAYER_HEIGHT
        )
        if player_2_rect.colliderect(ball_rect):
            ball.velocity.x = -ball.velocity.x

        # Check if ball goes out of bounds
        if ball.position.x - BALL_RADIUS <= 0:
            print("Player 2 scores!")
            self.reset_ball()

        elif ball.position.x + BALL_RADIUS >= SCREEN_WIDTH:
            print("Player 1 scores!")
            self.reset_ball()

        # Normalize ball velocity
        if ball.velocity.length() != 0:
            ball.velocity = ball.velocity.normalize() * BALL_SPEED

        ball.position += ball.velocity

    def reset_ball(self):
        """Reset ball to middle screen, with random direction"""
        angle = math.radians(random.randint(0, 360))
        self.state.ball.position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.state.ball.velocity = BALL_SPEED * Vector2(
            math.cos(angle), math.sin(angle)
        )

    def update_state(self, player_id, move):
        """Update the game state if currently running"""
        if self.running:
            self.update_ball()
            
            if player_id == PLAYER_1:
                self.state.player_1.y = max(
                    0,
                    min(
                        SCREEN_HEIGHT - PLAYER_HEIGHT,
                        self.state.player_1.y + move * PLAYER_SPEED,
                    ),
                )
            elif player_id == PLAYER_2:
                self.state.player_2.y = max(
                    0,
                    min(
                        SCREEN_HEIGHT - PLAYER_HEIGHT,
                        self.state.player_2.y + move * PLAYER_SPEED,
                    ),
                )
