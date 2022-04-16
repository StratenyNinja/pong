import pygame
import random
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
FONT_W = 10
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
        self.speed = [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


# Manager
class Manager:
    def __init__(self):
        self.running = True
        self.click = False
        self.logo_img = pygame.image.load("images/logo.png").convert_alpha()
        self.logo_rect = self.logo_img.get_rect()
        self.logo_rect.center = (WINDOW_W // 2, 165)
        self.start_img = pygame.image.load("images/start.png").convert_alpha()
        self.start_rect = self.start_img.get_rect()
        self.start_rect.center = (WINDOW_W // 2, 305)
        self.exit_img = pygame.image.load("images/exit.png").convert_alpha()
        self.exit_rect = self.exit_img.get_rect()
        self.exit_rect.center = (WINDOW_W // 2, 415)
        self.player1 = Paddle()
        self.player1.rect.x = BALL_DIAMETER * 2
        self.player1.rect.y = (WINDOW_H + STATS_H - PADDLE_H) // 2
        self.player2 = Paddle()
        self.player2.rect.x = WINDOW_W - BALL_DIAMETER * 2 - PADDLE_W
        self.player2.rect.y = (WINDOW_H + STATS_H - PADDLE_H) // 2
        self.ball = Ball()
        self.ball.rect.x = (WINDOW_W - BALL_DIAMETER) // 2
        self.ball.rect.y = (WINDOW_H + STATS_H - BALL_DIAMETER) // 2
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, self.ball)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

    def draw_menu(self):
        screen.fill(BLACK)
        screen.blit(self.logo_img, self.logo_rect)
        screen.blit(self.start_img, self.start_rect)
        screen.blit(self.exit_img, self.exit_rect)

    def draw_background(self):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (0, 0 + STATS_H, WINDOW_W, BORDER_H))
        pygame.draw.rect(screen, WHITE, (0, WINDOW_H - BORDER_H, WINDOW_W, BORDER_H))
        for i in range((WINDOW_H - STATS_H) // BORDER_H - 2):
            if i % 2 == 0:
                pygame.draw.rect(screen, WHITE, ((WINDOW_W - BORDER_H) // 2, i * BORDER_H + STATS_H, BORDER_H, BORDER_H))

    def key_pressed_p1(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.moveUp()
        if keys[pygame.K_s]:
            self.player1.moveDown()

    def key_pressed_p2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player2.moveUp()
        if keys[pygame.K_DOWN]:
            self.player2.moveDown()

    def ball_bounce(self):
        if self.ball.rect.top <= STATS_H + BORDER_H:
            self.ball.speed[1] = -self.ball.speed[1]
        if self.ball.rect.bottom >= WINDOW_H - BORDER_H:
            self.ball.speed[1] = -self.ball.speed[1]
        if self.ball.rect.left <= 0:
            self.ball.speed[0] = -self.ball.speed[0]
        if self.ball.rect.right >= WINDOW_W:
            self.ball.speed[0] = -self.ball.speed[0]
        if pygame.sprite.collide_mask(self.ball, self.player1) or pygame.sprite.collide_mask(self.ball, self.player2):
            self.ball.speed[0] = -self.ball.speed[0]


# Game
class Game:
    def __init__(self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.caption = pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.icon = pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.manager = Manager()

        while True:
            self.manager.check_events()
            self.manager.draw_menu()
            mx, my = pygame.mouse.get_pos()
            if self.manager.start_rect.collidepoint(mx, my):
                if self.manager.click:
                    while True:
                        self.manager.check_events()
                        self.manager.draw_background()
                        self.manager.key_pressed_p1()
                        self.manager.key_pressed_p2()
                        self.manager.ball_bounce()
                        self.manager.all_sprites.update()
                        self.manager.all_sprites.draw(screen)
                        pygame.display.update()
                        self.clock.tick(FPS)
            if self.manager.exit_rect.collidepoint(mx, my):
                if self.manager.click:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()