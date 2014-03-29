import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

from cv2tutorial.util import fetch_image

img = fetch_image(sys.argv[1])

images = []
titles = []

def add_img(image, title):
    global images, titles
    images.append(image)
    titles.append(title)

kernel = np.ones((5, 5), np.float32)/25

add_img(img, 'Original')
add_img(cv2.filter2D(img, -1, kernel), 'Average')
add_img(cv2.GaussianBlur(img, (5, 5), 0), 'Gaussian')
add_img(cv2.medianBlur(img, 5), 'Median')
add_img(cv2.bilateralFilter(img, 9, 75, 75), 'Bilateral')

for i in range(len(images)):
    plt.subplot(1, len(images), i)
    plt.imshow(images[i])
    plt.title(titles[i])

plt.show()
