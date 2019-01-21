import math
from Objects import *

class CollisionChecker:

    def checkBallAndTopWall(self, ball):
        if ball.position[1] - ball.radius < 0:
            ball.speed.down = -ball.speed.down

    def checkBallAndBottomWall(self, ball, screensize):
        if ball.position[1] + ball.radius > screensize[1]:
            ball.speed.down = -ball.speed.down

    def checkBallAndLeftWall(self, ball, paddle):
        if ball.position[0] - ball.radius < 0:
            if ball.position[1] > paddle.position.top and ball.position[1] < paddle.position.bottom:
                angle = (ball.position[1] - paddle.position.centery) / (paddle.position.height / 2)
                angle *= math.pi / 2
                cos = math.cos(angle)
                sin = math.sin(angle)
                r = math.sqrt(50)
                ball.setSpeed(Speed(cos * r, sin * r))
                ball.setPosition([ball.radius, ball.position[1]])

    def checkBallAndRightWall(self, ball, paddle, screensize):
        if ball.position[0] + ball.radius > screensize[0]:
            if ball.position[1] > paddle.position.top and ball.position[1] < paddle.position.bottom:
                angle = (ball.position[1] - paddle.position.centery) / (paddle.position.height / 2)
                angle *= math.pi / 2
                cos = math.cos(angle)
                sin = math.sin(angle)
                r = math.sqrt(50)
                ball.setSpeed(Speed(-cos * r, sin * r))
                ball.setPosition([screensize[0] - ball.radius, ball.position[1]])
