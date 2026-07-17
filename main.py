import pygame
import harvester
import math
harvester.start()

pygame.init()

WIDTH, HEIGHT = 600, 400
BAR_WIDTH = WIDTH - 20
FLASH_AT = 0.85
WHEEL_LOCK_DEG = 540
STEER_SMOOTH = 0.15 # fraction of the gap to the real input closed per frame
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 56)
panel_color = (40, 40, 40) # color for the panels: Gray
text_color = (255, 255, 255) # color for the text: White
bg_color = (15, 15, 15) # screen background, also used for the number plates
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

# static plates for the readouts, sized for the worst-case digit count

def make_plate(text_font, sample, pad_x=14, pad_y=8):
    w, h = text_font.size(sample)
    return pygame.Rect(0, 0, w + pad_x, h + pad_y)

rpm_plate = make_plate(big_font, "8888")
rpm_plate.midbottom = (rpm_rect.centerx, rpm_rect.bottom - 8)

speed_plate = make_plate(big_font, "888")
speed_plate.center = speed_rect.center

def draw_steering_panel(surface, steer, rect):
    pygame.draw.rect(surface, panel_color, rect)
    surface.blit(font.render("STEERING", True, text_color), (rect.left + 4, rect.top - LABEL_H))
    
    center = rect.center
    radius = min(rect.width, rect.height) // 2 - 10

    pygame.draw.circle(surface, (90, 90, 90), center, radius, width=4)
    
    rot = steer * WHEEL_LOCK_DEG
    
    for spoke_deg in (0, 180, 90):
        a = math.radians(spoke_deg + rot)
        end = (center[0] + radius * math.cos(a), center[1] + radius * math.sin(a))
        pygame.draw.line(surface, text_color, center, end, 4)
    
    a = math.radians(-90 + rot)
    tip = (center[0] + radius * math.cos(a), center[1] + radius * math.sin(a))
    inner = (center[0] + (radius - 12) * math.cos(a), center[1] + (radius - 12) * math.sin(a))
    pygame.draw.line(surface, (255, 40, 40), inner, tip, 6)
    
    pygame.draw.circle(surface, text_color, center, 6)

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

def flash_on(period_ms=150): # makes it so it alternates and doesnt rely on frames
    return (pygame.time.get_ticks() // period_ms) % 2 == 0
   
def blit_plated(surface, text_font, text, plate):
    pygame.draw.rect(surface, bg_color, plate, border_radius=4)
    text_surf = text_font.render(text, True, text_color)
    surface.blit(text_surf, text_surf.get_rect(center=plate.center))
   
def draw_rpm_panel(surface, rpm, frac, rect, plate):
    pygame.draw.rect(surface, panel_color, rect)
    surface.blit(font.render("RPM", True, text_color), (rect.left + 4, rect.top - LABEL_H))
    
    if frac >= FLASH_AT:
        fill_color = (255, 40, 40) if flash_on() else (255, 140, 0)
    else:
        fill_color = (0, 160, 70)
    
    fill_h = int(frac * rect.height) # height of the colored rectangle for the rpm
    pygame.draw.rect(surface, fill_color, pygame.Rect(rect.left, rect.bottom - fill_h, rect.width, fill_h))
    
    blit_plated(surface, big_font, f"{rpm:.0f}", plate)
    
def draw_speed_panel(surface, speed, rect, plate):
    pygame.draw.rect(surface, panel_color, rect)
    surface.blit(font.render("SPEED KM/H", True, text_color), (rect.left + 4, rect.top - LABEL_H))
    
    blit_plated(surface, big_font, f"{speed:.0f}", plate)
    
shown_steer = 0.0 # display-side steering that chases the raw input

running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
    screen.fill(bg_color)
    
    draw_trace(screen, harvester.gas_history, gas_rect, (0, 255, 0), "GAS")
    draw_trace(screen, harvester.brake_history, brake_rect, (255, 0, 0), "BRAKE")
    draw_rpm_panel(screen, harvester.latest["rpm"], harvester.latest["rpm_frac"], rpm_rect, rpm_plate)
    draw_speed_panel(screen, harvester.latest["speed"], speed_rect, speed_plate)
    shown_steer += (harvester.latest["steer"] - shown_steer) * STEER_SMOOTH
    draw_steering_panel(screen, shown_steer, steering_rect)
    
    pygame.display.flip()
    clock.tick(60)
                
pygame.quit()
