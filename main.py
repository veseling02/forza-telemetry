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
    min_x = min(x for x, y in world_points)
    max_x = max(x for x, y in world_points)
    min_y = min(y for x, y in world_points)
    max_y = max(y for x, y in world_points)
    if max_x == min_x or max_y == min_y:
        return []
    
    return [
        (
            (x - min_x) / (max_x - min_x) * screen_width,
            (y - min_y) / (max_y - min_y) * screen_height
        )
        for x, y in world_points
    ]
    
    
    
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
    screen.fill((15, 15, 15))
    print(f"outline: {len(harvester.track_outline)} | current lap points: {len(harvester.current_lap_points)}")
    
    if harvester.current_lap_points:
        print(harvester.current_lap_points[0])
        print(harvester.current_lap_points[-1])
    
    projected = get_track_projection(harvester.current_lap_points, WIDTH, HEIGHT)
    print(f"projected points: {len(projected)}")
    
    for point in projected:
        pygame.draw.circle(screen, (255, 255, 255), (int(point[0]), int(point[1])), 2)
    
    pygame.display.flip()
    clock.tick(60)
                
pygame.quit()
