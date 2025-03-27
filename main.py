import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import pygame
import static
import sys

class Keys:
    def __init__(self, keys: dict[str, int]) -> None:
        self.keys = keys

class MovementKeys(Keys):
    def __init__(self, u=pygame.K_w, l=pygame.K_a, d=pygame.K_s, r=pygame.K_d) -> None:
        self.up = u
        self.left = l
        self.down = d
        self.right = r


class Platform:
    def __init__(self, x: int, y: int, width: int, height: int, color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.hitbox)
    def colliderect(this, other):
        return this.hitbox.colliderect(other)

class Player:
    def __init__(self, x: int, y: int, color: pygame.Color = pygame.Color(128, 128, 0), keys: MovementKeys = MovementKeys(), speed: int=3) -> None:
        self.hitbox = pygame.Rect(x, y, 64, 96)
        self.color = color
        self.keys = keys
        self.speed = speed
        self.grav: int = 0
    def draw(self, screen: pygame.Surface, debug) -> None:
        pygame.draw.rect(screen, self.color, self.hitbox)
        if debug:
            pygame.draw.line(screen, pygame.Color(0, 255, 0), (self.hitbox.x, 0), (self.hitbox.x, screen.get_width()), 5)
            pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.hitbox.right, 0), (self.hitbox.right, screen.get_width()), 5)
            pygame.draw.line(screen, pygame.Color(0, 255, 255), (0, self.hitbox.y), (screen.get_width(), self.hitbox.y), 5)
            pygame.draw.line(screen, pygame.Color(255, 128, 196), (0, self.hitbox.bottom), (screen.get_width(), self.hitbox.bottom), 5)

            text = pygame.font.SysFont("courier new", 24).render(f"x: {self.hitbox.x}", True, pygame.Color(255, 255, 255))
            screen.blit(text, (0, self.hitbox.y - text.get_height()))
            text = pygame.font.SysFont("courier new", 24).render(f"y: {self.hitbox.y}", True, pygame.Color(255, 255, 255))
            screen.blit(text, (self.hitbox.right + 7, 0)) # Add padding (because of the width of the line)
    def update(self, screen, platforms) -> None:
        next_hitbox = self.hitbox.copy()
        keys = pygame.key.get_pressed()
        if keys[self.keys.up]:
            self.grav = -10
        
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
        
        self.grav += 1
        if self.grav > 0:
            next_hitbox.y += self.grav
            for platform in platforms:
                if platform.colliderect(next_hitbox):
                    next_hitbox.bottom = platform.hitbox.top
                    self.grav = 0
        else:
            next_hitbox.y += self.grav
            for platform in platforms:
                if platform.colliderect(next_hitbox):
                    next_hitbox.top = platform.hitbox.bottom
                    self.grav = 0

        self.hitbox = next_hitbox

def main() -> None:
    pygame.init()

    GLBL_KYS = Keys({
        "quit": pygame.K_b,
        "toggle debug": pygame.K_t,
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
                if GLBL_KYS.keys["quit"] == event.key:
                    running = False
                elif GLBL_KYS.keys["toggle debug"] == event.key:
                    debug = not debug

        player.update(screen, platforms)

        screen.blit(BG_IMG, (0, 0))
        player.draw(screen, debug)
        [platform.draw(screen) for platform in platforms]
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__": main()