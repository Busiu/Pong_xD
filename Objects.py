import pygame, math

class Speed:
    def __init__ (self, right, down):
        self.right = right
        self.down = down

class Ball:
    def __init__ (self, position, speed, color, radius):
        self.position = position
        self.speed = speed
        self.color = color
        self.radius = radius

    def draw(self, screen):
        x_floor = math.floor(self.position[0])
        y_floor = math.floor(self.position[1])
        pygame.draw.circle(screen, self.color, [x_floor, y_floor], self.radius)

    def updateSpeed(self):
        self.position[0] += self.speed.right
        self.position[1] += self.speed.down

    def setSpeed(self, speed):
        self.speed = speed

    def setPosition(self, position):
        self.position = position

class Paddle:
    def __init__(self, position, speed, color):
        self.position = position
        self.speed = speed
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.position)

    def update(self, vector):
        self.position.centerx += vector.right
        self.position.centery += vector.down