import random

from collections import deque
from time import sleep

import numpy as np
import cv2


img_height = 600
img_width = 600

# the 3 is for BGR?
img = np.zeros((img_width, img_height, 3), dtype=np.uint8)

def draw_line():
    point_1 = (0, 0)
    point_2 = (511, 511)
    blue = 255
    green = 0
    red = 0
    color = (blue, green, red)
    thickness = 5
    cv2.line(img, point_1, point_2, color, thickness)


def draw_rectangle():
    point_1 = (384, 0)
    point_2 = (510, 128)
    blue = 0
    green = 255
    red = 0
    color = (blue, green, red)
    thickness = 3
    cv2.rectangle(img, point_1, point_2, color, thickness)


def draw_circle(center):
    radius = 63
    blue = 0
    green = 0
    red = 255
    color = (blue, green, red)
    thickness = -1
    cv2.circle(img, center, radius, color, thickness)


def draw_ellipse():
    center = (256, 256)
    axes_lengths = (100, 50)
    rotation = 20 
    start_angle = 0
    end_angle = 180
    color = 255
    thickness = -1
    cv2.ellipse(img, center, axes_lengths, rotation, start_angle,
                end_angle, color, thickness)


def draw_polygon():
    points = np.array(
        [
            [10, 5],
            [20, 30],
            [70, 20],
            [50, 10],
        ],
        np.int32
    )
    points = points.reshape((-1, 1, 2))
    closed = True 
    blue = 0
    green = 255
    red = 255
    color = (blue, green, red)
    cv2.polylines(img, [points], closed, color)


def draw_text():
    origin = (10, 500)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 4
    color = (255, 255, 255)
    thickness = 2
    line_type = cv2.CV_AA
    cv2.putText(img, 'OpenCV', origin, font, font_scale,
                color, thickness, line_type)

draw_line()
draw_rectangle()
draw_ellipse()
draw_text()
draw_polygon()
x_0 = 449
y_0 = 63

draw_circle((x_0, y_0))

class Worm(object):
    def __init__(self, image, start, length,
                 cell_size, color, stringy=4):
        self.image = image
        self.x, self.y = start
        self.cells = [start]
        self.length = length
        self.cell_size = cell_size
        self.color = color
        self.stringy = stringy

        self.x_max = len(image) - cell_size
        self.y_max = len(image) - cell_size

        self.last_change = None

    def valid(self, point):
        x, y = point
        if x < 0 or x > self.x_max:
            return False

        if y < 0 or y > self.y_max:
            return False

        return True

    def random_next(self):
        x = self.cells[0][0]
        y = self.cells[0][1]

        new_point = [x, y]
        position = random.randint(0, 1)
        change = self.cell_size * random.choice([-1, 1])
        new_point[position] += change
        if self.valid(new_point):
            self.last_change = (position, change)
            return tuple(new_point)

        return (x, y)

    def next_cell(self):
        """Move either up or down."""

        # prefer previous choice
        if self.last_change is not None and random.randint(0, self.stringy) != 0:
            new_point = [self.cells[0][0], self.cells[0][1]]
            new_point[self.last_change[0]] += self.last_change[1]
            if self.valid(new_point):
                return tuple(new_point)
        
        return self.random_next()

    def add_cell(self):
        """Add a new cell at the front."""
        new = self.next_cell()
        self.cells.insert(0, new)
        self.draw_cell(new, self.color)

    def move(self):
        """Add a new cell and remove the oldest cell."""
        new = self.next_cell()
        self.cells.insert(0, new)
        old = self.cells.pop(-1)
        self.draw_cell(new, self.color)
        if old not in self.cells: # don't erase the body
            self.draw_cell(old, color=(0, 0, 0))

    def draw_cell(self, cell, color=None):
        """Draw a cell."""
        if color is None:
            color is self.color

        point_1 = (cell[0], cell[1])
        point_2 = (cell[0] + self.cell_size, cell[1] + self.cell_size)
        cv2.rectangle(self.image, point_1, point_2, color, -1)

    def update(self):
        if len(self.cells) < self.length:
            self.add_cell()
            return
        
        self.move()



cv2.imshow('image', img)

worms = [
    Worm(img,
        (300, 300), 200, 5, (
            random.randint(0, 256),
            random.randint(0, 256),
            random.randint(0, 256),
        ),
        stringy=20
    )
    for x in range(1)
]


while True:
    for worm in worms:
        worm.update()

    cv2.imshow('image', img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
