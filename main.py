import pygame
import harvester
import math

pygame.init()

WIDTH, HEIGHT = 600, 400
BAR_WIDTH = WIDTH - 20
x_step = BAR_WIDTH / 240
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forza Live Telemetry")

clock = pygame.time.Clock()
    
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
    screen.fill((15, 15, 15))
        
    pygame.draw.rect(screen, (40, 40, 40), (10, 10, BAR_WIDTH, 100))
    screen.blit(font.render("GAS", True, (255, 255, 255)), (10, 10))
    
    for index in range(1, len(harvester.gas_history)):
        x1 = 10 + (index - 1) * x_step
        x2 = 10 + index * x_step
        y1 = 10 + (1.0 - harvester.gas_history[index - 1]) * 100
        y2 = 10 + (1.0 - harvester.gas_history[index]) * 100
        pygame.draw.line(screen, (0, 255, 0), (int(x1), int(y1)), (int(x2), int(y2)))
        
    
    pygame.draw.rect(screen, (40, 40, 40), (10, 120, BAR_WIDTH, 100))
    screen.blit(font.render("BRAKE", True, (255, 255, 255)), (10, 120))
    
    for index in range(1, len(harvester.brake_history)):
        x1 = 10 + (index - 1) * x_step
        x2 = 10 + index * x_step
        y1 = 120 + (1.0 - harvester.brake_history[index - 1]) * 100
        y2 = 120 + (1.0 - harvester.brake_history[index]) *100
        pygame.draw.line(screen, (255, 0, 0), (int(x1), int(y1)), (int(x2), int(y2)))
        
    pygame.display.flip()
    clock.tick(60)
                
pygame.quit()
