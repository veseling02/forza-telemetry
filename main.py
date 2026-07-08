import pygame
import harvester

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forza Live Telemetry")

clock = pygame.time.Clock()

x_step = WIDTH / 240

def get_track_projection(world_points, screen_width, screen_height):
    if not world_points:
        return []

running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
    screen.fill((15, 15, 15))
                