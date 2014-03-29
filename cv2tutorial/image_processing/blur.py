import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

from cv2tutorial.util import fetch_image
from cv2tutorial.displayer import Displayer

img = fetch_image(sys.argv[1])

displayer = Displayer()

kernel = np.ones((5, 5), np.float32)/25

displayer.add_image(img, 'Original')
displayer.add_image(cv2.filter2D(img, -1, kernel), 'Average')
displayer.add_image(cv2.GaussianBlur(img, (5, 5), 0), 'Gaussian')
displayer.add_image(cv2.medianBlur(img, 5), 'Median')
displayer.add_image(cv2.bilateralFilter(img, 9, 75, 75), 'Bilateral')

displayer.display()
