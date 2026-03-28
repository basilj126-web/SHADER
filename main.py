import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class AlienShooter:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
        gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        self.clock = pygame.time.Clock()
        self.alien_positions = []
        self.bullets = []
        self.player_position = [0, 0]
        self.is_running = True

    def spawn_aliens(self):
        for _ in range(5):
            x = np.random.uniform(-2, 2)
            y = np.random.uniform(-1, 1)
            self.alien_positions.append([x, y, -10])

    def render_aliens(self):
        glColor3f(0.0, 1.0, 0.0)
        for pos in self.alien_positions:
            glBegin(GL_QUADS)
            glVertex3f(pos[0] - 0.1, pos[1] - 0.1, pos[2])
            glVertex3f(pos[0] + 0.1, pos[1] - 0.1, pos[2])
            glVertex3f(pos[0] + 0.1, pos[1] + 0.1, pos[2])
            glVertex3f(pos[0] - 0.1, pos[1] + 0.1, pos[2])
            glEnd()

    def render_player(self):
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex3f(self.player_position[0], self.player_position[1] - 0.1, -5)
        glVertex3f(self.player_position[0] - 0.1, self.player_position[1] + 0.1, -5)
        glVertex3f(self.player_position[0] + 0.1, self.player_position[1] + 0.1, -5)
        glEnd()

    def move_player(self, direction):
        if direction == 'LEFT' and self.player_position[0] > -2.5:
            self.player_position[0] -= 0.1
        elif direction == 'RIGHT' and self.player_position[0] < 2.5:
            self.player_position[0] += 0.1

    def shoot(self):
        self.bullets.append([self.player_position[0], self.player_position[1], -4])

    def render_bullets(self):
        glColor3f(1.0, 1.0, 0.0)
        for bullet in self.bullets[:]:
            bullet[2] += 0.15
            glBegin(GL_LINES)
            glVertex3f(bullet[0], bullet[1], bullet[2])
            glVertex3f(bullet[0], bullet[1], bullet[2]-0.1)
            glEnd()
            if bullet[2] > 0:
                self.bullets.remove(bullet)

    def check_collision(self):
        for bullet in self.bullets[:]:
            for alien in self.alien_positions[:]:
                if (alien[0] - 0.15 < bullet[0] < alien[0] + 0.15 and 
                    alien[1] - 0.15 < bullet[1] < alien[1] + 0.15 and 
                    alien[2] - 0.5 < bullet[2] < alien[2] + 0.5):
                    if alien in self.alien_positions:
                        self.alien_positions.remove(alien)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

    def run(self):
        self.spawn_aliens()
        pygame.display.set_caption("3D Alien Shooter")
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.is_running = False

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.move_player('LEFT')
            if keys[K_RIGHT]:
                self.move_player('RIGHT')
            if keys[K_SPACE]:
                self.shoot()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.render_aliens()
            self.render_player()
            self.render_bullets()
            self.check_collision()
            
            if not self.alien_positions:
                self.spawn_aliens()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = AlienShooter()
    game.run()