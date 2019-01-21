from Objects import *

DARK_GREEN = (0, 144, 0)
DARK_RED = (0, 0, 144)


class CollisionChecker:
    def __init__(self, screensize):
        self.screensize = screensize
        self.angle_coefficient = 0.8

    def checkBallAndTopWall(self, ball):
        if ball.position[1] - ball.radius < 0:
            ball.speed.down *= -1

    def checkBallAndBottomWall(self, ball):
        if ball.position[1] + ball.radius > self.screensize[1]:
            ball.speed.down *= -1

    def checkBallAndLeftWall(self, ball, paddle):
        if ball.speed.right > 0:
            return False
        if ball.position[0] - ball.radius < 0:
            if ball.position[0] + ball.radius < 0:
                return True
            else:
                if ball.position[0] > 0 and paddle.top < ball.position[1] < paddle.bottom:
                    angle = (ball.position[1] - paddle.centery) / (paddle.height / 2)
                    angle *= math.pi / 2 * self.angle_coefficient
                    cos = math.cos(angle)
                    sin = math.sin(angle)
                    r = math.sqrt(ball.speed.down**2 + ball.speed.right**2)
                    ball.setSpeed(Speed(cos * r, sin * r))
                    ball.setPosition([ball.radius, ball.position[1]])
                    ball.setPlayer(paddle.player)
        return False

    def checkBallAndRightWall(self, ball, paddle):
        if ball.speed.right < 0:
            return False
        if ball.position[0] + ball.radius > self.screensize[0]:
            if ball.position[0] - ball.radius > self.screensize[0]:
                return True
            else:
                if ball.position[0] < self.screensize[0] and paddle.top < ball.position[1] < paddle.bottom:
                    angle = (ball.position[1] - paddle.centery) / (paddle.height / 2)
                    angle *= math.pi / 2 * self.angle_coefficient
                    cos = math.cos(angle)
                    sin = math.sin(angle)
                    r = math.sqrt(ball.speed.down**2 + ball.speed.right**2)
                    ball.setSpeed(Speed(-cos * r, sin * r))
                    ball.setPosition([self.screensize[0] - ball.radius, ball.position[1]])
                    ball.setPlayer(paddle.player)
        return False
