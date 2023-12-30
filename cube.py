import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Initialize Pygame
pygame.init()
# Set up the window and OpenGL context
width, height = 800, 600
pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

class Particle:
    def __init__(self):
        self.position = [random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)]
        self.velocity = [random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)]
        self.size = 0.1

    def update(self):
        # Update particle position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]
        # Add gravity effect if needed

def create_particles(quantity):
    particles = []
    for _ in range(quantity):
        particles.append(Particle())
    return particles

def handle_controls(particles):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # Increase particle speed
        for particle in particles:
            particle.velocity = [v * 1.1 for v in particle.velocity]
    if keys[pygame.K_DOWN]:
        # Decrease particle speed
        for particle in particles:
            particle.velocity = [v * 0.9 for v in particle.velocity]
    if keys[pygame.K_RIGHT]:
        # Increase particle quantity
        particles.extend(create_particles(10))
    if keys[pygame.K_LEFT]:
        # Decrease particle quantity
        if len(particles) > 10:
            del particles[-10:]

def draw_square(position, size):
    glBegin(GL_QUADS)
    glVertex3f(position[0] - size / 2, position[1] - size / 2, position[2])
    glVertex3f(position[0] + size / 2, position[1] - size / 2, position[2])
    glVertex3f(position[0] + size / 2, position[1] + size / 2, position[2])
    glVertex3f(position[0] - size / 2, position[1] + size / 2, position[2])
    glEnd()

def draw_cube_outline():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_QUADS)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)

    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)

    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)

    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, -1, 1)

    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    glVertex3f(-1, 1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def render(particles):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_cube_outline()  # Draw cube outline here

    for particle in particles:
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)  # Set particle color (white)
        draw_square(particle.position, particle.size)
        glPopMatrix()

    pygame.display.flip()

def main():
    running = True
    particles = create_particles(100)
    gravity_enabled = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other user inputs

        handle_controls(particles)

        for particle in particles:
            particle.update()

        render(particles)

    pygame.quit()

if __name__ == "__main__":
    main()
