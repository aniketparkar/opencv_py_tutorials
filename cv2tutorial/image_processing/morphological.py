import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

from cv2tutorial.util import fetch_image

images = []
titles = []

def add_img(image, title):
    global images, titles
    images.append(image)
    titles.append(title)

orig = fetch_image(sys.argv[1], 0)
add_img(orig, 'Original')

square = np.ones((9, 9), np.float32)
rectangle = cv2.getStructuringElement(cv2.MORPH_RECT,(1,13))
ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
kernel = cross

add_img(cv2.erode(orig, kernel, iterations=1), 'Erosion')
add_img(cv2.dilate(orig, kernel, iterations=1), 'Dilation')
add_img(cv2.morphologyEx(orig, cv2.MORPH_OPEN, kernel), 'Opening')
closing = cv2.morphologyEx(orig, cv2.MORPH_CLOSE, kernel)
add_img(closing, 'Closing')
add_img(cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel), 'OpeningClosing')
add_img(cv2.morphologyEx(orig, cv2.MORPH_GRADIENT, kernel), 'Gradient')
add_img(cv2.morphologyEx(orig, cv2.MORPH_TOPHAT, kernel), 'Top Hat')
add_img(cv2.morphologyEx(orig, cv2.MORPH_BLACKHAT, kernel), 'Black Hat')

for i in range(len(images)):
    plt.subplot(1, len(images), i)
    plt.imshow(images[i])
    plt.title(titles[i])

plt.show()
