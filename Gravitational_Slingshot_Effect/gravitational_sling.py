import pygame
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 7
VEL_SCALE = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load assets
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

# Classes
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        # Update velocity and position
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    return Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)

def main():
    running = True
    clock = pygame.time.Clock()

    # Initialize objects
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        # Handle events
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        # Draw background
        win.blit(BG, (0, 0))

        # Preview new ship trajectory
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)
        
        # Move and draw objects
        for obj in objects[:]:
            obj.move(planet)
            obj.draw()

            # Remove objects if off-screen or colliding with the planet
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)

        # Draw the planet
        planet.draw()

        # Update the screen
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravitational Slingshot Effect")
    main()