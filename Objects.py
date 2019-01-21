import math
import cv2
import numpy as np
import random

class Speed:
    def __init__(self, right, down):
        self.right = right
        self.down = down


class Ball:
    def __init__(self, position, speed, radius, player=None):
        self.position = position
        self.speed = speed
        self.radius = radius
        self.player = player

    def draw(self, screen):
        x_floor = math.floor(self.position[0])
        y_floor = math.floor(self.position[1])
        if self.player is None:
            rand_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            cv2.circle(screen, (x_floor, y_floor), self.radius, rand_color, -1)
        else:
            cv2.circle(screen, (x_floor, y_floor), self.radius, self.player.color, -1)

    def updateSpeed(self):
        self.position[0] += self.speed.right
        self.position[1] += self.speed.down

    def setSpeed(self, speed):
        self.speed = speed

    def setPosition(self, position):
        self.position = position

    def setPlayer(self, player):
        self.player = player


class Paddle:
    def __init__(self, x, y, width, height, player):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player = player

        self.centery = y + height/2
        self.top = y
        self.bottom = y + height

    def draw(self, screen):
        cv2.rectangle(screen, (self.x, self.y), (self.x+self.width, self.bottom), self.player.color, -1)

    def update(self, y):
        self.y = y
        self.centery = y + self.height / 2
        self.top = y
        self.bottom = y + self.height


class Player:
    def __init__(self, color, points = 0):
        self.color = color
        self.points = points

    def add_point(self):
        self.points += 1


class ROITracker:
    def __init__(self, r, h, c, w, frame):
        self.track_window = (c, r, w, h)
        self.frame = frame
        roi = self.frame[r:r + h, c:c + w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        self.roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    def update_frame(self, frame):
        self.frame = frame

    def meanshift(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], self.roi_hist, [0, 180], 1)
        ret, self.track_window = cv2.meanShift(dst, self.track_window, self.term_crit)


class Screen:
    def __init__(self, width, height, roi_width, roi_height):
        self.width = width
        self.height = height
        self.roi_width = roi_width
        self.roi_height = roi_height

    def get_track_window(self):
        return int((self.width - self.roi_width) / 2), int((self.height - self.roi_height) / 2), self.roi_width, self.roi_height

    def align_roi(self, cap, key_confirm_code, delay):
        BLUE = (255, 0, 0)
        WHITE = (255, 255, 255)
        c, r, w, h = self.get_track_window()
        key_pressed = -1
        while key_pressed != key_confirm_code:
            ret, frame = cap.read()
            cv2.rectangle(frame, (c, r), (c + w, r + h), BLUE, 2)
            msg = 'Put your face in the rectangle, press space to confirm'
            cv2.putText(frame, msg, (20, self.height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, WHITE, 1, cv2.LINE_AA)
            cv2.imshow('real_view', frame)
            key_pressed = cv2.waitKey(delay) & 0xff
        return frame