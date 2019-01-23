from CollisionChecker import *
import cv2
import random


def random_speed_vector(value=math.sqrt(50)):
    b = [value/math.sqrt(2), value/math.sqrt(2)]
    angle = random.choice([random.uniform(math.pi/2, math.pi), random.uniform(1.5*math.pi, 2*math.pi)])
    cos = math.cos(angle)
    sin = math.sin(angle)
    return b[0]*cos-b[1]*sin, b[0]*sin+b[1]*cos


def add_random_ball(x, y, ball_list):
    ball_position = [x, y]
    s = random_speed_vector()
    ball_speed = Speed(s[0], s[1])
    ball = Ball(ball_position, ball_speed, 10)
    ball_list.append(ball)


def main():
    # CONFIG
    player1 = Player((0, 144, 0))
    player2 = Player((0, 0, 144))
    BLUE = (255, 0, 0)
    delay = 30  # 1s / fps
    key_confirm_code = 32  # opencv code for space key
    paddle_length = 160
    left_player_points = 0
    right_player_points = 0
    counter = 0
    spawn_freq = int(2500 / delay)

    screen = Screen(640, 480, 120, 160)  # resolution of the screen, size of the roi
    crwh0 = screen.get_track_window(0)  # parameters of the roi windows
    crwh1 = screen.get_track_window(1)

    cap = cv2.VideoCapture(0)

    frame = screen.align_roi(cap, key_confirm_code, delay)  # align roi with the face of the player
    tracker0 = ROITracker(crwh0[1], crwh0[3], crwh0[0], crwh0[2], frame)
    tracker1 = ROITracker(crwh1[1], crwh1[3], crwh1[0], crwh1[2], frame)

    ball_position = [screen.width/2, screen.height/2]
    s = random_speed_vector()
    ball_speed = Speed(s[0], s[1])
    ball = Ball(ball_position, ball_speed, 10)
    balls = [ball]

    paddle_left = Paddle(0, (screen.height - paddle_length)/2, 5, paddle_length, player1)
    paddle_right = Paddle(screen.width - 5, (screen.height - paddle_length)/2, 5, paddle_length, player2)

    collisionDetector = CollisionChecker((screen.width, screen.height))

    while True:
        ret, frame = cap.read()
        if ret:
            tracker0.update_frame(frame)
            tracker0.meanshift()

            tracker1.update_frame(frame)
            tracker1.meanshift()

            # Draw it on image
            x, y, w, h = tracker0.track_window
            cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
            paddle_left.update(y)

            x, y, w, h = tracker1.track_window
            cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
            paddle_right.update(y)

            for each_ball in balls:
                each_ball.updateSpeed()

            for each_ball in balls:
                collisionDetector.checkBallAndTopWall(each_ball)
                collisionDetector.checkBallAndBottomWall(each_ball)
                if collisionDetector.checkBallAndLeftWall(each_ball, paddle_left):
                    if each_ball.player == player2:
                        right_player_points += 1
                    balls.remove(each_ball)
                if collisionDetector.checkBallAndRightWall(each_ball, paddle_right):
                    if each_ball.player == player1:
                        left_player_points += 1
                    balls.remove(each_ball)

            for each_ball in balls:
                each_ball.draw(frame)

            paddle_left.draw(frame)
            paddle_right.draw(frame)

            msg = 'Pts: ' + str(left_player_points)
            cv2.putText(frame, msg, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, player1.color, 2, cv2.LINE_AA)
            msg = 'Pts: ' + str(right_player_points)
            cv2.putText(frame, msg, (screen.width - 80, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, player2.color, 2, cv2.LINE_AA)
            msg = 'Press Esc to exit, R to reset config'
            cv2.putText(frame, msg, (int(screen.width/2) - 170, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, BLUE, 2, cv2.LINE_AA)

            cv2.imshow('real_view', frame)

            counter += 1
            if counter % spawn_freq == 0:
                add_random_ball(screen.width / 2, screen.height / 2, balls)
                counter = 0

            k = cv2.waitKey(delay) & 0xff
            if k == ord('a'):
                add_random_ball(screen.width / 2, screen.height / 2, balls)

            if k == ord('r'):
                crwh0 = screen.get_track_window(0)  # parameters of the roi windows
                crwh1 = screen.get_track_window(1)

                cap = cv2.VideoCapture(0)

                frame = screen.align_roi(cap, key_confirm_code, delay)  # align roi with the face of the player
                tracker0 = ROITracker(crwh0[1], crwh0[3], crwh0[0], crwh0[2], frame)
                tracker1 = ROITracker(crwh1[1], crwh1[3], crwh1[0], crwh1[2], frame)

                ball_position = [screen.width / 2, screen.height / 2]
                s = random_speed_vector()
                ball_speed = Speed(s[0], s[1])
                ball = Ball(ball_position, ball_speed, 10)
                balls = [ball]

                paddle_left = Paddle(0, (screen.height - paddle_length) / 2, 5, paddle_length, player1)
                paddle_right = Paddle(screen.width - 5, (screen.height - paddle_length) / 2, 5, paddle_length, player2)

                collisionDetector = CollisionChecker((screen.width, screen.height))

                left_player_points = 0
                right_player_points = 0
                counter = 0

                ret, frame = cap.read()

            if k == 27:
                cv2.imwrite("final_screen.jpg", frame)
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()


main()
