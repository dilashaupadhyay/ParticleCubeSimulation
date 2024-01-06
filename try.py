import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up perspective projection
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Define cube vertices
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

# Define edges of the cube
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

# Define a particle class
class Particle:
    def __init__(self):
        self.position = [random.uniform(-0.5, 0.5) for _ in range(3)]  # Random initial position
        self.velocity = [random.uniform(-0.1, 0.1) for _ in range(3)]  # Random initial velocity

    def update(self):
        for i in range(3):
            self.position[i] += self.velocity[i]
            # Bound the particles within the cube
            if abs(self.position[i]) >= 1:
                self.velocity[i] *= -1

# Create a list of particles
num_particles = 100
particles = [Particle() for _ in range(num_particles)]

# Function to draw the cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw particles
def draw_particles():
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)  # Particle color
    for particle in particles:
        glVertex3fv(particle.position)
    glEnd()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(1, 3, 1, 1)  # Rotate the cube

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()

    for particle in particles:
        particle.update()
    draw_particles()

    pygame.display.flip()
    pygame.time.wait(10)
# ... (previous code)

# Define initial settings
particle_speed = 0.1
point_size = 2
simulation_running = True
gravity_enabled = False
restitution_enabled = True
repulsion_enabled = True

# Function to handle button click events for additional functionalities
def handle_click(pos):
    global num_particles, particle_speed, point_size, simulation_running
    global gravity_enabled, restitution_enabled, repulsion_enabled
    x, y = pos
    if 10 <= x <= 110 and 10 <= y <= 40:
        num_particles += 10  # Increase particles by 10 when clicked
    # Add more button handling logic for decreasing particles, adjusting speed, size, etc.
    elif 10 <= x <= 210 and 90 <= y <= 120:
        gravity_enabled = not gravity_enabled  # Toggle gravity
    elif 230 <= x <= 430 and 90 <= y <= 120:
        restitution_enabled = not restitution_enabled  # Toggle restitution
    elif 450 <= x <= 650 and 90 <= y <= 120:
        repulsion_enabled = not repulsion_enabled  # Toggle repulsion

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_click(pygame.mouse.get_pos())

    glRotatef(1, 3, 1, 1)  # Rotate the cube

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()

    if simulation_running:
        for particle in particles:
            particle.update(gravity_enabled, restitution_enabled, repulsion_enabled)
    draw_particles()

    # Drawing buttons
    pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (10, 10, 100, 30))
    # Add more button drawing code for adjusting particles, speed, size, etc.
    pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255) if gravity_enabled else (255, 0, 0), (10, 90, 200, 30))
    pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255) if restitution_enabled else (255, 0, 0), (230, 90, 200, 30))
    pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255) if repulsion_enabled else (255, 0, 0), (450, 90, 200, 30))

    pygame.display.flip()
    pygame.time.wait(10)
 
 