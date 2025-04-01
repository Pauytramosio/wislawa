import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import pygame
import static
import sys

from maps import *

from enum import Enum

#%% imgs

images = {
    name: pygame.image.load(static.static["images"][name])
    for name in static.static["images"]
}
print("loaded images:", images)

#%%

class Gamemode(Enum):
    PLAY = 1
    WIN  = 2

class Keys:
    def __init__(self, keys: dict[str, int]) -> None:
        self.keys = keys

class MovementKeys(Keys):
    def __init__(self, u=pygame.K_w, l=pygame.K_a, d=pygame.K_s, r=pygame.K_d) -> None:
        self.up = u
        self.left = l
        self.down = d
        self.right = r

def maxmin(val, max, min): return max if val > max else min if val < min else val

class Player:
    def __init__(self, x: int, y: int, color: pygame.Color = pygame.Color(128, 128, 0), keys: MovementKeys = MovementKeys(), speed: int=3) -> None:
        self.hitbox = pygame.Rect(x, y, 64, 96)
        self.color = color
        self.keys = keys
        self.speed = speed
        self.grav: int = 0
        self.hp: int = 20
    def draw(self, screen: pygame.Surface, debug) -> None:
        screen.blit(images["player"], (self.hitbox.x, self.hitbox.y))
        heartimg = images["heart"]
        pen = 0
        for i in range(self.hp):
            screen.blit(heartimg, (pen, 0))
            pen += heartimg.get_width()
        if debug:
            pygame.draw.rect(screen, self.color, self.hitbox)

            pygame.draw.line(screen, pygame.Color(0, 255, 0), (self.hitbox.x, 0), (self.hitbox.x, screen.get_width()), 5)
            pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.hitbox.right, 0), (self.hitbox.right, screen.get_width()), 5)
            pygame.draw.line(screen, pygame.Color(0, 255, 255), (0, self.hitbox.y), (screen.get_width(), self.hitbox.y), 5)
            pygame.draw.line(screen, pygame.Color(255, 128, 196), (0, self.hitbox.bottom), (screen.get_width(), self.hitbox.bottom), 5)

            text = pygame.font.SysFont("courier new", 24).render(f"x: {self.hitbox.x}", True, pygame.Color(255, 255, 255))
            screen.blit(text, (0, maxmin(self.hitbox.y - text.get_height(), screen.get_height() - text.get_height(), 0))) # Add padding (because of the height of the line)
            text = pygame.font.SysFont("courier new", 24).render(f"y: {self.hitbox.y}", True, pygame.Color(255, 255, 255))
            screen.blit(text, (maxmin(self.hitbox.right + 7, screen.get_width() - text.get_width(), 0), 0)) # Add padding (because of the width of the line)


            pygame.draw.rect(screen, self.color, self.hitbox)
            text = pygame.font.SysFont("courier new", 24).render(f"hp: {self.hp}", True, pygame.Color(255, 255, 255))
            screen.blit(text, (self.hitbox.x + 5, self.hitbox.y + 5))
            
    def update(self, screen, platforms) -> None:
        next_hitbox = self.hitbox.copy()
        keys = pygame.key.get_pressed()
        
        if keys[self.keys.left]:
            next_hitbox.x -= self.speed
            for platform in platforms:
                if platform.colliderect(next_hitbox):
                    next_hitbox.x = platform.hitbox.right
        if keys[self.keys.right]:
            next_hitbox.x += self.speed
            for platform in platforms:
                if platform.colliderect(next_hitbox):
                    next_hitbox.right = platform.hitbox.x
        
        on_ground = False
        for platform in platforms:
            if platform.colliderect(pygame.Rect(next_hitbox.x, next_hitbox.y + 1, next_hitbox.width, next_hitbox.height)):
                on_ground = True
                next_hitbox.bottom = platform.hitbox.top
                break
        
        if (not on_ground) or (on_ground and self.grav < 0):
            self.grav += 1
            next_hitbox.y += self.grav
            for platform in platforms:
                if platform.colliderect(next_hitbox):
                    next_hitbox.bottom = platform.hitbox.top
                    self.hp -= self.grav // static.static["player-damage-modifier"]
                    self.grav = 0
                    break
        else:
            self.hp -= self.grav // static.static["player-damage-modifier"]
            self.grav = -20 if keys[self.keys.up] else 0

        self.hitbox = next_hitbox

def main() -> None:
    pygame.init()

    gamemode: Gamemode = Gamemode.PLAY

    KEYS = Keys({
        "quit": pygame.K_b,
    })

    debug: bool = False

    screen = pygame.display.set_mode(static.static["screen-size"])
    pygame.display.set_caption(static.static["screen-title"])

    player: Player = Player(0, 0)

    platforms: list[Platform] = [
        Platform(0, screen.get_height()-32, screen.get_width(), 32, pygame.Color(0, 128, 0)),
        Platform(500, 0, 100, 32, pygame.Color(0, 128, 0)),
        ]

    BG_IMG = pygame.image.load(static.static["background"])
    BG_IMG = pygame.transform.scale(BG_IMG, static.static["screen-size"])

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if KEYS.keys["quit"] == event.key:
                    running = False
        
        keys_pressed = pygame.key.get_pressed()
        debug = keys_pressed[pygame.K_t]

        if gamemode == Gamemode.PLAY:
            player.update(screen, platforms)
            gamemode = Gamemode.WIN if player.hp <= 0 else gamemode
            screen.blit(BG_IMG, (0, 0))
            player.draw(screen, debug)
            [platform.draw(screen) for platform in platforms]
        
        elif gamemode == Gamemode.WIN:
            wintxt = pygame.font.SysFont("courier new", 32).render("you win (also you are dead)", True, (0, 0, 0))
            screen.blit(wintxt, ((screen.get_width() - wintxt.get_width()) / 2, (screen.get_height() - wintxt.get_height()) / 2))

        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()