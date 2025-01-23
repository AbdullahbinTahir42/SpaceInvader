import pygame
import sys
import random
import math
from pygame import mixer

class SpaceInvaderGame:
    def __init__(self):
        pygame.init()
        
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invader")
        self.icon = pygame.image.load("ufo.png")
        pygame.display.set_icon(self.icon)

        self.background = pygame.image.load("background.png")
        mixer.music.load("back_sound.wav")
        mixer.music.play(-1)

        self.player = Player(self.width, self.height)
        self.enemies = [Enemy() for _ in range(8)]
        self.bullet = Bullet()

        self.explosion_image = pygame.image.load("Blst.png")
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.over_font = pygame.font.Font("freesansbold.ttf", 64)
        self.restart_font = pygame.font.Font("freesansbold.ttf", 40)

        self.running = True
        self.paused = False

    def restart_game(self):
        self.player.reset_position()
        self.bullet.reset()
        self.score = 0
        for enemy in self.enemies:
            enemy.reset()

    def show_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        restart_text = self.restart_font.render("Press R to RESTART", True, (255, 255, 255))
        self.screen.blit(over_text, (210, 268))
        self.screen.blit(restart_text, (210, 380))

    def show_pause(self):
        pause_font = pygame.font.Font("freesansbold.ttf", 64)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(pause_text, (270, 255))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                else:
                    self.player.handle_keydown(event.key, self.bullet)
            if event.type == pygame.KEYUP:
                self.player.handle_keyup(event.key)

    def update(self):
        if not self.paused:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            self.player.update_position(self.width)
            self.player.draw(self.screen)

            for enemy in self.enemies:
                enemy.update_position()
                if enemy.y > 440:
                    for e in self.enemies:
                        e.y = 2000
                    self.show_game_over()
                    return

                if self.bullet.state == "fire" and enemy.check_collision(self.bullet):
                    mixer.Sound("explosion.wav").play()
                    self.screen.blit(self.explosion_image, (enemy.x, enemy.y))
                    self.score += 10
                    enemy.reset()
                    self.bullet.reset()

                enemy.draw(self.screen)

            self.bullet.update_position()
            self.bullet.draw(self.screen)

            self.show_score()
        else:
            self.show_pause()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


class Player:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("spaceship.png")
        self.x = screen_width // 2 - 32
        self.y = screen_height - 100
        self.x_change = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update_position(self, screen_width):
        self.x += self.x_change
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - 64:
            self.x = screen_width - 64

    def handle_keydown(self, key, bullet):
        if key == pygame.K_LEFT:
            self.x_change = -7
        elif key == pygame.K_RIGHT:
            self.x_change = 7
        elif key == pygame.K_SPACE:
            if bullet.state == "ready":
                mixer.Sound("b_sound.wav").play()
                bullet.fire(self.x, self.y)

    def handle_keyup(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.x_change = 0

    def reset_position(self):
        self.x = 368
        self.y = 500
        self.x_change = 0


class Enemy:
    def __init__(self):
        self.image = pygame.image.load("art.png")
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)
        self.x_change = 7
        self.y_change = 40

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update_position(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= 736:
            self.x_change *= -1
            self.y += self.y_change

    def check_collision(self, bullet):
        distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
        return distance < 27

    def reset(self):
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 150)


class Bullet:
    def __init__(self):
        self.image = pygame.image.load("bullet.png")
        self.x = 0
        self.y = 510
        self.y_change = 25
        self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x, self.y))

    def update_position(self):
        if self.state == "fire":
            self.y -= self.y_change
            if self.y <= 0:
                self.reset()

    def fire(self, x, y):
        self.state = "fire"
        self.x = x + 16
        self.y = y - 10

    def reset(self):
        self.state = "ready"
        self.y = 510


if __name__ == "__main__":
    game = SpaceInvaderGame()
    game.run()
