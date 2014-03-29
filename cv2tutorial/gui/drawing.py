from random import (
    choice,
    randint,
)

from collections import deque
from time import sleep

import numpy as np
import cv2

from cv2tutorial.util import fetch_image

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve.

def main():
    global mode, drawing
    cap = cv2.VideoCapture(0)

    ret, img = cap.read()
    worm_image = np.zeros(img.shape, img.dtype)

    image_width = len(img[0])
    image_height = len(img)

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


    def bdraw_circle(center):
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

    bdraw_circle((x_0, y_0))

    X = 0
    Y = 1

    class Worm(object):
        def __init__(self, image, start, length,
                     cell_size, color, stringy=4):
            self.image = image
            self.x, self.y = start
            self.cells = []
            self.length = length
            self.cell_size = cell_size
            self.color = color
            self.stringy = stringy

            self.x_max = len(image[0]) - cell_size
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
            if len(self.cells) > 0:
                x = self.cells[0][X]
                y = self.cells[0][Y]
            else:
                x = self.x
                y = self.y

            new_point = [x, y]
            position = randint(0, 1)
            change = self.cell_size * choice([-1, 1])
            new_point[position] += change
            if self.valid(new_point):
                self.last_change = (position, change)
                return tuple(new_point)

            return (x, y)

        def next_cell(self):
            """Move either up or down."""

            # prefer previous choice
            if len(self.cells) > 0 and self.last_change is not None and randint(0, self.stringy) != 0:
                new_point = [self.cells[0][X], self.cells[0][Y]]
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
            if not old in self.cells:
                self.draw_cell(old, color=(0, 0, 0))
            self.draw_cell(new)

        def draw_cell(self, cell, color=None):
            """Draw a cell."""
            if color is None:
                color is self.color

            point_1 = (cell[X], cell[Y])
            point_2 = (cell[X] + self.cell_size, cell[Y] + self.cell_size)
            cv2.rectangle(self.image, point_1, point_2, color, -1)

        def update(self):
            if len(self.cells) < self.length:
                self.add_cell()
            elif len(self.cells) == 0:
                return
            
            self.move()
            
            for cell in self.cells:
                self.draw_cell(cell, self.color)

        def change_length(self, new_length):
            cur_len = len(self.cells)
            if new_length > cur_len:
                for _ in range(new_length - cur_len):
                    self.add_cell()
            elif new_length < self.length:
                for _ in range(cur_len - new_length):
                    cell = self.cells.pop(-1)
                    self.draw_cell(cell, color=(0, 0, 0))
                    if len(self.cells) == 0:
                        self.x, self.y = cell
            self.length = length

        def erase(self):
            for cell in self.cells:
                self.draw_cell(cell, color=(0, 0, 0))



    cv2.imshow('image', img)

    def adjust_worm_count(worm_list, count, length, stringy):
        if len(worm_list) < count:
            for _ in range(count - len(worm_list)):
                worm = Worm(worm_image,
                            (randint(0, image_width), randint(0,image_height)),
                            length, 5, (
                                randint(0, 256),
                                randint(0, 256),
                                randint(0, 256),
                            ),
                        stringy=stringy
                )
                worm_list.append(worm)
                worm.update()
        elif len(worm_list) > count:
            for i in range(len(worm_list) - count):
                worm = worm_list.pop()
                worm.erase()


    def adjust_worm_length(worm_list, length):
        for worm in worm_list:
            worm.change_length(length)

    def adjust_worm_stringy(worm_list, stringy):
        for worm in worm_list:
            worm.stringy = stringy


    def nothing(x):
        pass

    cv2.createTrackbar('count', 'image', 0, 1000, nothing)
    cv2.createTrackbar('length', 'image', 0, 2000, nothing)
    cv2.createTrackbar('stringy', 'image', 0, 1000, nothing)

    worms = []
    old_length = 0
    old_stringy = 0


    def paint(x, y):
        global ix, iy, mode
        if mode == True:
            cv2.rectangle(worm_image, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv2.circle(worm_image, (x, y), 5, (0, 0, 255), -1)

    # mouse callback function
    def draw_circle(event, x, y, flags, param):
        global ix, iy, drawing, mode

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                paint(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            paint(x, y)


    cv2.setMouseCallback('image', draw_circle)

    cap_mode = True

    def masked_add(bg_img, fg_img):
        # create mask and inverse mask of fg
        fg_gray = cv2.cvtColor(fg_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(fg_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # black out the area of fg in bg
        bg = cv2.bitwise_and(bg_img, bg_img, mask=mask_inv)

        fg = cv2.bitwise_and(fg_img, fg_img, mask=mask)

        final = cv2.addWeighted(bg_img, 0.3, fg, 0.7, 0)

        final = cv2.add(bg, fg)
        return final


    while True:
        if cap_mode:
            ret, img = cap.read()

        count = cv2.getTrackbarPos('count', 'image')
        length = cv2.getTrackbarPos('length', 'image')
        stringy = cv2.getTrackbarPos('stringy', 'image')

        adjust_worm_count(worms, count, length, stringy)

        if old_length != length:
            adjust_worm_length(worms, length)
            old_length = length

        if old_stringy != stringy:
            adjust_worm_stringy(worms, stringy)
            old_stringy = stringy

        for worm in worms:
            worm.update()

        final_img = masked_add(img, worm_image)

        cv2.imshow('image', final_img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        if k == ord('r'):
            img[:,:,:] = fetch_image('domo_kun.jpg')
        if k == ord('p'):
            cap_mode = not cap_mode

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
