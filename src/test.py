import sys

import pygame

screen = pygame.display.set_mode((1200, 800))
pygame.init()
pygame.display.set_caption("Test")
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_q:
                sys.exit()

        pygame.display.flip()
