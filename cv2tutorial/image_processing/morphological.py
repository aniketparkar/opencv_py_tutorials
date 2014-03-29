import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

from cv2tutorial.util import fetch_image
from cv2tutorial.displayer import Displayer

def main():
    displayer = Displayer()

    orig = fetch_image(sys.argv[1], 0)
    displayer.add_image(orig, 'Original')

    square = np.ones((9, 9), np.float32)
    rectangle = cv2.getStructuringElement(cv2.MORPH_RECT,(1,13))
    ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    kernel = cross

    displayer.add_image(cv2.erode(orig, kernel, iterations=1), 'Erosion')
    displayer.add_image(cv2.dilate(orig, kernel, iterations=1), 'Dilation')
    displayer.add_image(cv2.morphologyEx(orig, cv2.MORPH_OPEN, kernel), 'Opening')
    closing = cv2.morphologyEx(orig, cv2.MORPH_CLOSE, kernel)
    displayer.add_image(closing, 'Closing')
    displayer.add_image(cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel), 'OpeningClosing')
    displayer.add_image(cv2.morphologyEx(orig, cv2.MORPH_GRADIENT, kernel), 'Gradient')
    displayer.add_image(cv2.morphologyEx(orig, cv2.MORPH_TOPHAT, kernel), 'Top Hat')
    displayer.add_image(cv2.morphologyEx(orig, cv2.MORPH_BLACKHAT, kernel), 'Black Hat')

    displayer.display(cmap='gray')

if __name__ == '__main__':
    main()
