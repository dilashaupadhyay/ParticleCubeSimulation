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

    def update(self, gravity, repulsion):
        # Update particle position based on velocity
        for i in range(3):
            self.position[i] += self.velocity[i]
            # Bound the particles within the cube and reflect velocities on collision
            if abs(self.position[i]) >= 1:
                self.velocity[i] *= -1

        # Apply gravity
        if gravity:
            self.velocity[1] -= 0.005

        # Apply repulsion between particles
        if repulsion:
            for particle in particles:
                if particle != self:
                    dist = sum((self.position[i] - particle.position[i]) ** 2 for i in range(3))
                    if dist < 0.1:
                        for i in range(3):
                            self.velocity[i] += (self.position[i] - particle.position[i]) * 0.01

# Create a list of particles
num_particles = 100
particles = [Particle() for _ in range(num_particles)]

# Simulation settings
gravity_on = False
repulsion_on = False

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:  # Toggle gravity on/off (press 'g')
                gravity_on = not gravity_on
            elif event.key == pygame.K_r:  # Toggle repulsion on/off (press 'r')
                repulsion_on = not repulsion_on

    glRotatef(1, 3, 1, 1)  # Rotate the cube

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()

    for particle in particles:
        particle.update(gravity_on, repulsion_on)
    draw_particles()

    pygame.display.flip()
    pygame.time.wait(10)
