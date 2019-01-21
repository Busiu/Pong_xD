import sys
import time
import random
import numpy as np
import cv2


width = 640
height = 480
ball_radius = 15
paddle_width = 70
paddle_height = 15

face_catch_width = 120
face_catch_height = 160

key_confirm_code = 32  # space
font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX

x_ball = 15
y_ball = 45
y_speed = 5
x_speed = 5

cap = cv2.VideoCapture(0)

# setup initial location of window
r, h, c, w = int((height-face_catch_height)/2), face_catch_height, int((width-face_catch_width)/2), face_catch_width   # simply hardcoded the values
track_window = (c, r, w, h)

# set the tracking
k = -1
while k != key_confirm_code:
    ret, frame = cap.read()
    img2 = cv2.rectangle(frame, (c, r), (c + w, r + h), 255, 2)
    cv2.putText(frame, 'Put your face in the rectangle, press space to confirm', (20, height - 10), font, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('real_view', frame)
    k = cv2.waitKey(60) & 0xff

# set up the ROI for tracking
roi = frame[r:r + h, c:c + w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while 1:
    ret, frame = cap.read()
    y_ball += y_speed
    x_ball += x_speed

    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x, y, w, h = track_window
        img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)

        cv2.circle(frame, (x_ball, y_ball), 15, (0, 0, 255), -1)
        img2 = cv2.rectangle(frame, (x, 0), (x + paddle_width, paddle_height), (0, 255, 0), -1)
        img2 = cv2.rectangle(frame, (x, height - paddle_height), (x + paddle_width, height), (0, 255, 0), -1)
        cv2.imshow('real_view', frame)
        print((x, y))
        if y_ball >= height - ball_radius - paddle_height or y_ball <= ball_radius + paddle_height:
            if x <= x_ball <= x+paddle_width:
                y_speed *= -1
            else:
                print("You lost")
                cv2.destroyAllWindows()
                sys.exit()
        if x_ball >= width - ball_radius or x_ball <= ball_radius:
            x_speed *= -1

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            cv2.imwrite(chr(k) + ".jpg", img2)
            break
    else:
        break

cv2.destroyAllWindows()
cap.release()
