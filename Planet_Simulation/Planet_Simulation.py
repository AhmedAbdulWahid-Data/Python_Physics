import pygame
import math

# Initialize pygame
pygame.init()

# Set up constants and the display window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Color constants
WHITE = (255, 255, 255)
YELLOW = (255, 190, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Font for displaying text
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    """
    A class representing a planet in the simulation.
    """

    AU = 149.6e6 * 1000   # Astronomical Unit in meters
    G = 6.67428e-11       # Gravitational constant
    SCALE = 250 / AU       # Scaling factor (1 AU = 250 pixels)
    TIMESTEP = 3600 * 24   # Time step (1 day in seconds)

    def __init__(self, x, y, radius, color, mass):
        """
        Initialize a planet object.
        :param x: Initial x position
        :param y: Initial y position
        :param radius: Radius of the planet
        :param color: Color of the planet
        :param mass: Mass of the planet
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False  # Flag to indicate if it's the Sun
        self.distance_to_sun = 0  # Distance to the Sun
        self.x_vel = 0  # Initial velocity in the x direction
        self.y_vel = 0  # Initial velocity in the y direction

    def draw(self, win):
        """
        Draw the planet and its orbit on the screen.
        :param win: The pygame window
        """
        # Scale the planet's position for display
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw the planet's orbit (only if there are enough points)
        if len(self.orbit) > 2:
            updated_points = [(px * self.SCALE + WIDTH / 2, py * self.SCALE + HEIGHT / 2) for px, py in self.orbit]
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet itself
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # If it's not the Sun, display the distance to the Sun
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        """
        Calculate the gravitational force exerted on this planet by another planet.
        :param other: The other planet to calculate the force with
        :return: The force components (x, y)
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        # Gravitational force formula
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        """
        Update the position of the planet based on gravitational forces.
        :param planets: A list of all planets in the simulation
        """
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocities based on the total forces
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update the planet's position
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Append the new position to the orbit list
        self.orbit.append((self.x, self.y))

        # Limit the orbit list length to 1000 points to prevent memory overflow
        if len(self.orbit) > 1000:
            self.orbit.pop(0)


def main():
    """
    Main function to run the simulation.
    """
    run = True
    clock = pygame.time.Clock()

    # Create the Sun and planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000  # Earth's orbital speed

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000  # Mars's orbital speed

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000  # Mercury's orbital speed

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000  # Venus's orbital speed

    planets = [sun, earth, mars, mercury, venus]

    # Main simulation loop
    while run:
        clock.tick(60)  # 60 FPS
        WIN.fill((0, 0, 0))  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update and draw each planet
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()  # Refresh the display

    pygame.quit()


if __name__ == "__main__":
    main()