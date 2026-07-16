import pygame
import harvester
import math
harvester.start()

pygame.init()

WIDTH, HEIGHT = 600, 400
BAR_WIDTH = WIDTH - 20
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 56)
panel_color = (40, 40, 40) # color for the panels: Gray
text_color = (255, 255, 255) # color for the text: White
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forza Live Telemetry")

clock = pygame.time.Clock()

MARGIN = 10
GAP = 10
LABEL_H = font.get_height() + 4

# top row gas|brake

gas_rect = pygame.Rect(MARGIN, MARGIN + LABEL_H, BAR_WIDTH, 100)
brake_rect = pygame.Rect(MARGIN, gas_rect.bottom + GAP + LABEL_H, BAR_WIDTH, 100)

# bottom row rpm|speed|steering

panel_w = (BAR_WIDTH - 2 * GAP) // 3 # width of the 3 panels while taking in account the gaps
panel_top = brake_rect.bottom + GAP + LABEL_H # where the bottom panels start 
panel_h = HEIGHT - panel_top - MARGIN # panel height using all the space left and leaving a gap at the bottom

rpm_rect = pygame.Rect(MARGIN, panel_top, panel_w, panel_h)
speed_rect = pygame.Rect(rpm_rect.right + GAP, panel_top, panel_w, panel_h)
steering_rect = pygame.Rect(speed_rect.right + GAP, panel_top, panel_w, panel_h)


def draw_trace(surface, history, rect, color, label):
    values = list(history)
    pygame.draw.rect(surface, panel_color, rect)
    surface.blit(font.render(label, True, text_color), (rect.left + 4, rect.top - LABEL_H))
    step = rect.width / (len(values) - 1)
    for i in range (1, len(values)):
        x1 = rect.left + (i - 1) * step
        x2 = rect.left + i * step
        y1 = rect.top + (1.0 - values[i - 1]) * rect.height
        y2 = rect.top + (1.0 - values[i]) * rect.height
        
        # build points that are needed for the draw.line function
        p1 = (int(x1), int(y1))
        p2 = (int(x2), int(y2)) 
        
        pygame.draw.line(surface, color, p1, p2)
    
def draw_rpm_panel(surface, rpm, frac, rect):
    pygame.draw.rect(surface, panel_color, rect)
    surface.blit(font.render("RPM", True, text_color), (rect.left + 4, rect.top - LABEL_H))
    text = big_font.render(f"{rpm:.0f}", True, text_color)
    surface.blit(text, text.get_rect(center=rect.center))
    
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
    screen.fill((15, 15, 15))
    
    draw_trace(screen, harvester.gas_history, gas_rect, (0, 255, 0), "GAS")
    draw_trace(screen, harvester.brake_history, brake_rect, (255, 0, 0), "BRAKE")
    draw_rpm_panel(screen, harvester.latest["rpm"], harvester.latest["rpm_frac"], rpm_rect)
    pygame.draw.rect(screen, panel_color, speed_rect)
    pygame.draw.rect(screen, panel_color, steering_rect)
    
    
    pygame.display.flip()
    clock.tick(60)
                
pygame.quit()
