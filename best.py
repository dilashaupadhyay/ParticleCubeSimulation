import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

class Particle:
    def __init__(self):
        self.position = [random.uniform(-0.5, 0.5) for _ in range(3)]
        self.velocity = [random.uniform(-0.1, 0.1) for _ in range(3)]
        self.color = (random.random(), random.random(), random.random())  # Random RGB color

    def update(self, gravity_on):
        for i in range(3):
            self.position[i] += self.velocity[i]
            if abs(self.position[i]) >= 1:
                self.velocity[i] *= -1
        if gravity_on:
            self.velocity[1] -= 0.01

class ParticleSimulation:
    def __init__(self, num_particles):
        self.gravity_on = True
        self.particles = [Particle() for _ in range(num_particles)]
        self.vertices = (
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        )
        self.edges = (
            (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
            (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
        )

    def distance(self, p1, p2):
        return math.sqrt(sum((p1.position[i] - p2.position[i]) ** 2 for i in range(3)))

    def handle_collisions(self):
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.distance(self.particles[i], self.particles[j]) < 0.1:
                    self.particles[i].velocity, self.particles[j].velocity = self.particles[j].velocity, self.particles[i].velocity

    def draw_cube(self):
        glLineWidth(3)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def draw_particles(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        for particle in self.particles:
            glColor3fv(particle.color)  # Use the color of the particle
            glVertex3fv(particle.position)
        glEnd()

    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

        font = pygame.font.Font(None, 36)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.gravity_on = not self.gravity_on
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.particles.append(Particle())
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        if self.particles:
                            self.particles.pop()

            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube()

            self.handle_collisions()
            for particle in self.particles:
                particle.update(self.gravity_on)
            self.draw_particles()

            text = font.render('Gravity ON' if self.gravity_on else 'Gravity OFF', True, (255, 255, 255))
            text_rect = text.get_rect(center=(display[0] / 2, 50))
            pygame.display.get_surface().blit(text, text_rect)

            pygame.display.flip()
            pygame.time.wait(10)

if __name__ == "__main__":
    sim = ParticleSimulation(100)
    sim.run()
    