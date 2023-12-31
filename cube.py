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
        self.position = [
            random.uniform(-0.05, 0.05),  # X coordinate within the cube
            random.uniform(-0.05, 0.05),  # Y coordinate within the cube
            random.uniform(-0.05, 0.05)   # Z coordinate within the cube
        ]
        self.velocity = [
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01)
        ]
        self.size = 0.01

    def update(self):
        # Update particle position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]
        
        # Constrain particle within the cube outline
        cube_half_size = 0.05
        for i in range(3):
            if self.position[i] < -cube_half_size:
                self.position[i] = -cube_half_size
                self.velocity[i] *= -1  # Reverse velocity to simulate bouncing off walls
            elif self.position[i] > cube_half_size:
                self.position[i] = cube_half_size
                self.velocity[i] *= -1  # Reverse velocity to simulate bouncing off walls

def create_particles(quantity):
    particles = []
    for _ in range(quantity):
        particles.append(Particle())
    return particles

def draw_cube_outline(size):
    half_size = size / 2
    vertices = [
        [-half_size, -half_size, -half_size],
        [half_size, -half_size, -half_size],
        [half_size, half_size, -half_size],
        [-half_size, half_size, -half_size],
        [-half_size, -half_size, half_size],
        [half_size, -half_size, half_size],
        [half_size, half_size, half_size],
        [-half_size, half_size, half_size]
    ]
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]

    glColor3f(1.0, 1.0, 1.0)  # Set outline color to white
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def render(particles):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_cube_outline(0.1)  # Draw the cube outline of 100mm

    for particle in particles:
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)  # Set particle color (white)
        glTranslatef(particle.position[0], particle.position[1], particle.position[2])
        glutSolidSphere(particle.size, 20, 20)  # Rendering particles as spheres
        glPopMatrix()

    pygame.display.flip()

def main():
    running = True
    particles = create_particles(500)  # Increased particles for better visibility
    gravity_enabled = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other user inputs

        for particle in particles:
            particle.update()

        render(particles)
        pygame.display.update()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()
