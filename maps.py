import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame
import chars

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int, color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.hitbox)
    def colliderect(this, other):
        return this.hitbox.colliderect(other)