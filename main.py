import pygame
import harvester

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forza Live Telemetry")

clock = pygame.time.Clock()

x_step = WIDTH / 240

running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
