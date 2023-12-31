import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class Particle:
    def __init__(self):
        self.position = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
        self.velocity = [random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)]

    def update(self):
        for i in range(3):
            self.position[i] += self.velocity[i]
            # Particle bounces off the walls if it reaches the boundary of the cube
            if abs(self.position[i]) >= 1:
                self.velocity[i] *= -1

def draw_cube():
    # ... (same cube drawing code as before)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    particles = [Particle() for _ in range(50)]  # Create 50 particles

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for particle in particles:
            particle.update()

        glRotatef(1, 3, 1, 1)  # Rotate the cube slightly
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()

        # Draw particles
        glBegin(GL_POINTS)
        glColor3f(1, 1, 1)
        for particle in particles:
            glVertex3fv(particle.position)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
