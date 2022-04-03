import pygame
import sys


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Main variables
WINDOW_W = 730
WINDOW_H = 530
FPS = 60

# Game variables
BORDER_W = WINDOW_W
BORDER_H = 10
PADDLE_W = 10
PADDLE_H = 100
BALL_RADIUS = 10
PADDLE_SPEED = 5
BALL_SPEED = 5

pygame.init()
window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    window.fill(BLACK)
    pygame.display.update()
    clock.tick(FPS)