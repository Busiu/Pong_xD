import pygame

class CollisionChecker:

    def checkPaddleAndBall(self, paddle, ball):
        if pygame.Rect.colliderect(paddle.position, ball.position):

            if (ball.period == 0):
                ball.speed.down = -ball.speed.down
            else:
                ball.speed.right = -ball.speed.right
            ball.period = (ball.period + 1) % 2

    def checkBallAndWalls(self, ball, screenSize):
        if (ball.position.right > screenSize[0] or
            ball.position.left < 0 or
            ball.position.bottom > screenSize[1] or
            ball.position.top < 0):

            if (ball.period == 0):
                ball.speed.down = -ball.speed.down
            else:
                ball.speed.right = -ball.speed.right
            ball.period = (ball.period + 1) % 2