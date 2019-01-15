import pygame, sys

class Speed:
    def __init__ (self, down, right):
        self.down = down
        self.right = right

class Ball:
    def __init__ (self, position, speed, color):
        self.position = position
        self.speed = speed
        self.color = color
        self.period = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.position)

    def update(self):
        self.position.centery += self.speed.down
        self.position.centerx += self.speed.right

class Paddle:
    def __init__(self, position, speed, color):
        self.position = position
        self.speed = speed
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.position)

    def update(self, vector):
        self.position.centerx += vector.down
        self.position.centery += vector.right