from Objects import *
from CollisionChecker import *

def main():
    pygame.init()
    FPS = 300
    clock = pygame.time.Clock()

    screen_size = (1280, 720)
    screen = pygame.display.set_mode(screen_size)

    DARK_GREEN = (0, 144, 0)                ## Color of paddles
    GREEN = (0, 255, 0)                     ## Color of ball
    BLACK = (0, 0, 0)                       ## Color of background

    ball_position = pygame.Rect(0, 0, 64, 64)
    ball_speed = Speed(5, 5)
    ball = Ball(ball_position, ball_speed, GREEN)

    paddle1_position = pygame.Rect(0, 300, 30, 120)
    paddle1_speed = Speed(0, 0)
    paddle1 = Paddle(paddle1_position, paddle1_speed, DARK_GREEN)

    paddle2_position = pygame.Rect(1250, 300, 30, 120)
    paddle2_speed = Speed(0, 0)
    paddle2 = Paddle(paddle2_position, paddle2_speed, DARK_GREEN)

    collisionDetector = CollisionChecker()

    while True:
        ## Update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w]):
            paddle1.update(Speed(0, -10))
        if(keys[pygame.K_s]):
            paddle1.update(Speed(0, 10))
        if(keys[pygame.K_UP]):
            paddle2.update(Speed(0, -10))
        if(keys[pygame.K_DOWN]):
            paddle2.update(Speed(0, 10))

        ball.update()

        ## Check Collisions
        collisionDetector.checkPaddleAndBall(paddle1, ball)
        collisionDetector.checkPaddleAndBall(paddle2, ball)
        collisionDetector.checkBallAndWalls(ball, screen_size)

        ## Draw
        screen.fill(BLACK)
        ball.draw(screen)
        paddle1.draw(screen)
        paddle2.draw(screen)

        ## Render
        pygame.display.update()

        ## Wait for another frame
        clock.tick(FPS)

main()