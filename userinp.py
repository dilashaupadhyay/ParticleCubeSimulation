import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

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
num_particles = 200
particles = [Particle() for _ in range(num_particles)]

# Function to check distance between particles
def distance(p1, p2):
    return math.sqrt(sum((p1.position[i] - p2.position[i]) ** 2 for i in range(3)))

# Function to handle particle collisions
def handle_collisions():
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            if distance(particles[i], particles[j]) < 0.1:  # Adjust the collision distance as needed
                # Swap velocities of colliding particles
                particles[i].velocity, particles[j].velocity = particles[j].velocity, particles[i].velocity

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
    glPointSize(5)  # Increase the size of the particles
    glBegin(GL_POINTS)
    for particle in particles:
        glColor3fv((1.0, 1.0, 1.0))  # Set particles to white color
        glVertex3fv(particle.position)
    glEnd()

# Function to handle user input
def handle_input():
    global num_particles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Green button for fewer particles
    if 50 <= mouse_x <= 150 and 50 <= mouse_y <= 100 and click[0] == 1:
        num_particles = 100  # Set fewer particles
        reset_particles()

    # Red button for more particles
    elif 200 <= mouse_x <= 300 and 50 <= mouse_y <= 100 and click[0] == 1:
        num_particles = 300  # Set more particles
        reset_particles()

# Function to reset particles based on the user input
def reset_particles():
    global particles
    particles = [Particle() for _ in range(num_particles)]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    handle_input()  # Check for user input
    glRotatef(1, 3, 1, 1)  # Rotate the cube

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()

    handle_collisions()  # Check and handle collisions
    for particle in particles:
        particle.update()
    draw_particles()

# Define a particle class
class Particle:
    def __init__(self):
        self.position = [random.uniform(-0.5, 0.5) for _ in range(3)]  # Random initial position
        self.velocity = [random.uniform(-0.1, 0.1) for _ in range(3)]  # Random initial velocity
        self.color = (random.random(), random.random(), random.random())  # Random RGB color

        # Ensure particles are initialized within the cube's boundaries
        for i in range(3):
            if abs(self.position[i]) > 0.5:
                self.position[i] *= 0.5 / abs(self.position[i])


    # Draw buttons
    pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (50, 50, 100, 50))  # Green button for fewer particles
    pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (200, 50, 100, 50))  # Red button for more particles

    pygame.display.flip()
    pygame.time.wait(10)
