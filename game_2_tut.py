# game.py
from config import *
import pygame
from pygame.locals import *
import time
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = BLUE
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((WINDOW_WIDTH - PADDLE_WIDTH) / 2, WINDOW_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = RED
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    def move(self, dx):
        if 0 <= self.rect.x + dx <= WINDOW_WIDTH - PADDLE_WIDTH:
            self.rect.x += dx
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = GREEN
        self.vx = BALL_X_VELOCITY
        self.vy = BALL_Y_VELOCITY
    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Wall collision detection
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.vx = -self.vx
        if self.rect.top <= 0:
            self.vy = -self.vy
    def check_collision(self, blocks, paddle, game):
        # Check for collision with paddle
        if self.rect.colliderect(paddle.rect):
            self.vy = -self.vy
            self.rect.bottom = paddle.rect.top  # Adjust ball position to avoid sticking
        # Check for collision with bricks
        for block in blocks:
            if self.rect.colliderect(block.rect):
                blocks.remove(block)
                self.vy = -self.vy
                game.score += 10
                break
        # Check for game over condition (ball goes past the paddle)
        if self.rect.top > WINDOW_HEIGHT:
            game.running = False
class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.score = 0
        pygame.display.set_caption("Breakout")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(WHITE)
        self.blocks = self.create_blocks()
        self.paddle = Paddle()
        self.ball = Ball()
        self.font = pygame.font.Font(None, 36)
    def create_blocks(self):
        blocks = []
        for row in range(ROWS_OF_BRICKS):
            for col in range(BRICKS_PER_ROW):
                x = col * (BRICK_WIDTH + BRICK_GUTTER_WIDTH) + BRICK_GUTTER_WIDTH
                y = row * (BRICK_HEIGHT + BRICK_GUTTER_WIDTH) + BRICK_Y_OFFSET
                blocks.append(Block(x, y))
        return blocks
    def draw_blocks(self):
        for block in self.blocks:
            block.draw(self.surface)
    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.surface.blit(score_text, (10, 10))
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.paddle.move(-10)
                    if event.key == K_RIGHT:
                        self.paddle.move(10)
            self.surface.fill(WHITE)
            self.draw_blocks()
            self.paddle.draw(self.surface)
            self.ball.move()
            self.ball.check_collision(self.blocks, self.paddle, self)
            self.ball.draw(self.surface)
            self.draw_score()
            pygame.display.flip()
            time.sleep(SLEEP_TIME)
        pygame.quit()
        self.show_game_over()

if __name__ == "__main__":
    game = Game()
    game.run()