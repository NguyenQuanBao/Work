import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Né chướng ngoại vật")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)


FONT = pygame.font.SysFont('Arial', 36)


CLOCK = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_button(text, x, y, w, h):
    pygame.draw.rect(SCREEN, BLACK, (x, y, w, h))
    label = FONT.render(text, True, WHITE)
    SCREEN.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)


def start_screen():
    while True:
        SCREEN.fill(WHITE)
        title = FONT.render("BẮT ĐẦU GAME", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        start_btn = draw_button("Bắt đầu", 200, 300, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        CLOCK.tick(60)


def game_over_screen():
    while True:
        SCREEN.fill(WHITE)
        title = FONT.render("GAME OVER", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        retry_btn = draw_button("Chơi lại", 200, 300, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        CLOCK.tick(60)


def main_game():
    player = Player()
    player_group = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()

    score = 0
    obstacle_timer = 0

    while True:
        SCREEN.fill(WHITE)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        player_group.update(keys)
        obstacles.update()


        obstacle_timer += 1
        if obstacle_timer > 30:
            obstacles.add(Obstacle())
            obstacle_timer = 0


        if pygame.sprite.spritecollide(player, obstacles, False):
            break  # Game over


        player_group.draw(SCREEN)
        obstacles.draw(SCREEN)


        score += 1
        score_text = FONT.render(f"Điểm: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        CLOCK.tick(60)


while True:
    start_screen()
    main_game()
    game_over_screen()
