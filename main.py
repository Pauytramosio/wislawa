import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""

import pygame
import static
import sys

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(static.static["screen-size"])
    pygame.display.set_caption(static.static["screen-title"])
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_b:
                        running = False
        pygame.display.update()
        clock.tick()
    pygame.quit()
    sys.exit()

if __name__ == "__main__": main()