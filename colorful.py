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
        self.color = (random.random(), random.random(), random.random())  # Random RGB color

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
    glLineWidth(3)  # Set line width to make the outline thicker
    glColor3f(1, 1, 1)  # Set color to white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw particles
def draw_particles():
    glPointSize(2)
    glBegin(GL_POINTS)
    for particle in particles:
        glColor3fv(particle.color)  # Use particle's color
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
