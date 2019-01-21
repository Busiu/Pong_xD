from Objects import *
from CollisionChecker import *

def main():
    pygame.init()
    FPS = 60
    clock = pygame.time.Clock()

    screen_size = (1280, 720)
    screen = pygame.display.set_mode(screen_size)

    DARK_GREEN = (0, 144, 0)                ## Color of paddles
    GREEN = (0, 255, 0)                     ## Color of ball
    BLACK = (0, 0, 0)                       ## Color of background

    ball_position = [100, 100]
    ball_speed = Speed(5, 5)
    ball = Ball(ball_position, ball_speed, GREEN, 10)

    paddle_left_position = pygame.Rect(0, 300, 5, 120)
    paddle_left_speed = Speed(0, 0)
    paddle_left = Paddle(paddle_left_position, paddle_left_speed, DARK_GREEN)

    paddle_right_position = pygame.Rect(1275, 300, 5, 120)
    paddle_right_speed = Speed(0, 0)
    paddle_right = Paddle(paddle_right_position, paddle_right_speed, DARK_GREEN)

    collisionDetector = CollisionChecker()

    while True:
        ## Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w]):
            paddle_left.update(Speed(0, -10))
        if(keys[pygame.K_s]):
            paddle_left.update(Speed(0, 10))
        if(keys[pygame.K_UP]):
            paddle_right.update(Speed(0, -10))
        if(keys[pygame.K_DOWN]):
            paddle_right.update(Speed(0, 10))

        ball.updateSpeed()

        ## Check Collisions
        collisionDetector.checkBallAndTopWall(ball)
        collisionDetector.checkBallAndBottomWall(ball, screen_size)
        collisionDetector.checkBallAndLeftWall(ball, paddle_left)
        collisionDetector.checkBallAndRightWall(ball, paddle_right, screen_size)

        ## Draw
        screen.fill(BLACK)
        ball.draw(screen)
        paddle_left.draw(screen)
        paddle_right.draw(screen)

        ## Render
        pygame.display.update()

        ## Wait for another frame
        clock.tick(FPS)

main()