import pygame
import pygame_gui
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbital Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

TRAIL_LENGTH = 150

# Body class
class Body:
    def __init__(self, x, y, mass, radius, color, vx, vy):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy
        self.trail = []

    def draw(self, screen):
        for i in range(len(self.trail) - 1):
            start_pos = self.trail[i]
            end_pos = self.trail[i + 1]
            alpha = 255 - i * 255 // TRAIL_LENGTH
            color = (*self.color[:3], alpha)
            pygame.draw.line(screen, color, start_pos, end_pos, 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

    def apply_gravity(self, other, G, dt):
        dx = other.x - self.x
        dy = other.y - self.y
        distance_sqr = max(dx**2 + dy**2, 1e-6)
        force = G * self.mass * other.mass / distance_sqr
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt

# Constants
G = 10e-11  # Gravitational constant

# Create bodies
bodies = [
    Body(WIDTH // 2, HEIGHT // 2, 1e14, 10, YELLOW, 0, 0),
]

# Collision handling
def handle_collisions(bodies):
    to_remove = []
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            dx = bodies[i].x - bodies[j].x
            dy = bodies[i].y - bodies[j].y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < bodies[i].radius + bodies[j].radius:
                merge_bodies(bodies, i, j, to_remove)
    for index in sorted(to_remove, reverse=True):
        del bodies[index]


def merge_bodies(bodies, i, j, to_remove):
    if i in to_remove or j in to_remove:
        return
    body1 = bodies[i]
    body2 = bodies[j]
    new_mass = body1.mass + body2.mass
    new_radius = (body1.radius**3 + body2.radius**3)**(1/3)
    new_vx = (body1.vx * body1.mass + body2.vx * body2.mass) / new_mass
    new_vy = (body1.vy * body1.mass + body2.vy * body2.mass) / new_mass
    new_color = [(body1.color[k] + body2.color[k]) // 2 for k in range(3)]
    bodies[i] = Body(body1.x, body1.y, new_mass, int(new_radius), new_color, new_vx, new_vy)
    to_remove.append(j)

# Main loop
running = True
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH - 210, HEIGHT - 50), (200, 30)),
    start_value=1,
    value_range=(0.1, 5),
    manager=manager
)

dragging = False
start_pos = None

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            end_pos = pygame.mouse.get_pos()
            dragging = False
            if start_pos:
                x, y = start_pos
                dx = end_pos[0] - x
                dy = end_pos[1] - y
                distance = math.sqrt(dx**2 + dy**2)
                if distance == 0:
                    distance = 10e-6
                v_tan = math.sqrt(G * 1e13 / distance) + random.uniform(-0.1, 0.1)
                bodies.append(Body(
                    x, y,  # x and y position
                    10**random.uniform(5.5, 8),  # mass
                    10,  # radius
                    (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),  # random color
                    -dx / 10, -dy / 10  # velocity
                ))
        manager.process_events(event)  # Process events for pygame_gui

    # Get the simulation speed from the slider
    sim_speed = slider.get_current_value()
    dt *= sim_speed

    # Apply gravity
    for body in bodies:
        for other in bodies:
            if body != other:
                body.apply_gravity(other, G, dt)

    handle_collisions(bodies)  # Handle collisions

    # Update positions
    for body in bodies:
        body.update_position(dt)

    # Draw everything
    screen.fill(BLACK)
    for body in bodies:
        body.draw(screen)
    manager.update(dt)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
