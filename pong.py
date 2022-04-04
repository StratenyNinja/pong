import pygame
import sys


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Main variables
WINDOW_W = 880
WINDOW_H = 670
FPS = 60


# Game variables
STATS_H = 100
SCORE_W = 30
SCORE_H = 50
BORDER_H = 10
PADDLE_W = 10
PADDLE_H = 100
BALL_DIAMETER = 10
PADDLE_SPEED = 4
BALL_SPEED = 4


# Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_W, PADDLE_H])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def moveUp(self):
        if self.rect.top > STATS_H + BORDER_H:
            self.rect.top -= PADDLE_SPEED

    def moveDown(self):
        if self.rect.bottom < WINDOW_H - BORDER_H:
            self.rect.bottom += PADDLE_SPEED


# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_DIAMETER, BALL_DIAMETER])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = [BALL_SPEED, BALL_SPEED]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

pygame.init()
window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

def draw_lines():
    pygame.draw.rect(window, WHITE, (0, 0, BORDER_W, BORDER_H))
    pygame.draw.rect(window, WHITE, (0, WINDOW_H - BORDER_H, BORDER_W, BORDER_H))
    for i in range((WINDOW_H - BORDER_H * 2) // BORDER_H):
        if i % 2 == 0:
            pygame.draw.rect(window, WHITE, ((WINDOW_W - BORDER_H) // 2, i * BORDER_H, BORDER_H, BORDER_H))

paddle1 = Paddle()
paddle1.rect.x = PADDLE_W
paddle1.rect.y = WINDOW_H // 2 - PADDLE_H // 2
paddle2 = Paddle()
paddle2.rect.x = WINDOW_W - PADDLE_W * 2
paddle2.rect.y = WINDOW_H // 2 - PADDLE_H // 2
ball = Ball()
ball.rect.x = WINDOW_W // 2
ball.rect.y = WINDOW_H // 2

all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1)
all_sprites.add(paddle2)
all_sprites.add(ball)

score1 = 0
score2 = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.moveUp()
    if keys[pygame.K_s]:
        paddle1.moveDown()
    if keys[pygame.K_UP]:
        paddle2.moveUp()
    if keys[pygame.K_DOWN]:
        paddle2.moveDown() 

    all_sprites.update()

    if ball.rect.x <= 0:
        score2 += 1
        ball.speed[0] = -ball.speed[0]
    if ball.rect.x >= WINDOW_W - BALL_RADIUS * 2:
        score1 += 1
        ball.speed[0] = -ball.speed[0]
    if ball.rect.y <= BORDER_H:
        ball.speed[1] = -ball.speed[1]
    if ball.rect.y >= WINDOW_H - BALL_RADIUS * 2 - BORDER_H:
        ball.speed[1] = -ball.speed[1]

    if pygame.sprite.collide_mask(ball, paddle1) or pygame.sprite.collide_mask(ball, paddle2):
        ball.bounce()

    window.fill(BLACK)
    draw_lines()

    all_sprites.draw(window)
    
    font = pygame.font.Font(None, 74)
    text = font.render(str(score1), 1, WHITE)
    window.blit(text, (250,10))
    text = font.render(str(score2), 1, WHITE)
    window.blit(text, (420,10))

    pygame.display.update()
    clock.tick(FPS)