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
BORDER_H = 10
PADDLE_SPEED = 4
BALL_SPEED = 4


# Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/paddle.png").convert_alpha()
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
        self.image = pygame.image.load("images/ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


# Manager
class Manager:
    def __init__(self):
        self.click = False
        self.game_mode_running = False
        self.game_running = False
        self.pause_running = False
        self.logo_img = pygame.image.load("images/logo.png").convert_alpha()
        self.logo_rect = self.logo_img.get_rect()
        self.logo_rect.center = (WINDOW_W // 2, self.logo_rect.height * 2)
        self.start_img = pygame.image.load("images/start.png").convert_alpha()
        self.start_rect = self.start_img.get_rect()
        self.start_rect.center = (WINDOW_W // 2, self.logo_rect.bottom + 70 + self.start_rect.height // 2)
        self.exit_img = pygame.image.load("images/exit.png").convert_alpha()
        self.exit_rect = self.exit_img.get_rect()
        self.exit_rect.center = (WINDOW_W // 2, self.start_rect.bottom + 20 + self.exit_rect.height // 2)
        self.pause_img = pygame.image.load("images/pause.png").convert_alpha()
        self.pause_rect = self.pause_img.get_rect()
        self.pause_rect.center = (WINDOW_W // 2, self.pause_rect.height * 2)
        self.resume_img = pygame.image.load("images/resume.png").convert_alpha()
        self.resume_rect = self.resume_img.get_rect()
        self.resume_rect.center = (WINDOW_W // 2, self.pause_rect.bottom + 70 + self.resume_rect.height // 2)
        self.restart_img = pygame.image.load("images/restart.png").convert_alpha()
        self.restart_rect = self.restart_img.get_rect()
        self.restart_rect.center = (WINDOW_W // 2, self.resume_rect.bottom + 20 + self.restart_rect.height // 2)
        self.main_menu_img = pygame.image.load("images/main_menu.png").convert_alpha()
        self.main_menu_rect = self.main_menu_img.get_rect()
        self.main_menu_rect.center = (WINDOW_W // 2, self.restart_rect.bottom + 20 + self.main_menu_rect.height // 2)
        self.vs_img = pygame.image.load("images/vs.png").convert_alpha()
        self.vs_rect = self.vs_img.get_rect()
        self.vs_rect.center = (WINDOW_W // 3, WINDOW_H // 2)
        self.cpu_img = pygame.image.load("images/cpu.png").convert_alpha()
        self.cpu_rect = self.cpu_img.get_rect()
        self.cpu_rect.center = (WINDOW_W // 3 * 2, WINDOW_H // 2)
        self.back_img = pygame.image.load("images/back.png").convert_alpha()
        self.back_rect = self.back_img.get_rect()
        self.back_rect.center = (WINDOW_W // 2, self.vs_rect.bottom + 20 + self.back_rect.height // 2)
        self.pause_symbol_img = pygame.image.load("images/pause_symbol.png").convert_alpha()
        self.pause_symbol_rect = self.pause_symbol_img.get_rect()
        self.pause_symbol_rect.center = (WINDOW_W // 2, self.pause_symbol_rect.height - 20)
        self.player1 = Paddle()
        self.player1.rect.x = self.player1.rect.width * 2
        self.player1.rect.y = WINDOW_H // 2
        self.player2 = Paddle()
        self.player2.rect.x = WINDOW_W - self.player1.rect.width * 3
        self.player2.rect.y = WINDOW_H // 2
        self.ball = Ball()
        self.ball.rect.x = (WINDOW_W - self.player1.rect.width) // 2
        self.ball.rect.y = (WINDOW_H + STATS_H - self.ball.rect.height) // 2
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, self.ball)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_mode_running:
                        self.game_mode_running = False
                    if self.game_running:
                        self.pause_running = True
                    if self.pause_running:
                        self.pause_running = False

    def draw_menu(self):
        screen.fill(BLACK)
        screen.blit(self.logo_img, self.logo_rect)
        screen.blit(self.start_img, self.start_rect)
        screen.blit(self.exit_img, self.exit_rect)

    def draw_game(self):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (0, STATS_H, WINDOW_W, BORDER_H))
        pygame.draw.rect(screen, WHITE, (0, WINDOW_H - BORDER_H, WINDOW_W, BORDER_H))
        for i in range((WINDOW_H - STATS_H) // BORDER_H - 2):
            if i % 2 == 0:
                pygame.draw.rect(screen, WHITE, ((WINDOW_W - BORDER_H) // 2, i * BORDER_H + STATS_H, BORDER_H, BORDER_H))
        screen.blit(self.pause_symbol_img, self.pause_symbol_rect)

    def draw_game_mode(self):
        screen.fill(BLACK)
        screen.blit(self.vs_img, self.vs_rect)
        screen.blit(self.cpu_img, self.cpu_rect)
        screen.blit(self.back_img, self.back_rect)

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
            self.manager.click = False

            self.manager.check_events()
            self.manager.draw_menu()

            mx, my = pygame.mouse.get_pos()

            # Game mode
            if self.manager.start_rect.collidepoint(mx, my) and self.manager.click:
                self.manager.game_mode_running = True
                while self.manager.game_mode_running:
                    self.manager.click = False

                    self.manager.check_events()
                    self.manager.draw_game_mode()

                    mx, my = pygame.mouse.get_pos()

                    # VS Game

                    # CPU Game

                    # Back
                    if self.manager.back_rect.collidepoint(mx, my):
                        if self.manager.click:
                            self.manager.game_mode_running = False
                            self.manager.click = False

                    pygame.display.update()
                    self.clock.tick(FPS)

            # Exit
            if self.manager.exit_rect.collidepoint(mx, my):
                if self.manager.click:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()