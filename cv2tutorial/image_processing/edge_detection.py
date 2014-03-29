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

orig = cv2.cvtColor(fetch_image(sys.argv[1]), cv2.COLOR_BGR2GRAY)

add_img(orig, 'Original')


img = cv2.bilateralFilter(np.float32(orig), 9, 75, 75)



x_kernel = np.array([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]])

y_kernel = np.array([[ 1,  2,  1],
                     [ 0,  0,  0],
                     [-1, -2, -1]])
"""
x_kernel = np.array([[3, 10, 3],
                     [0, 0, 0],
                     [-3, -10, -3]])

y_kernel = np.array([[ -3,  -0,  3],
                     [ -10,  0,  10],
                     [ -3, -0, 3]])
"""

"""
y_kernel = x_kernel = np.array([[ 0.5, 1, 0.5],
                                [ 1, -6, 1],
                                [ 0.5, 1, 0.5]])
"""

x_gradient = cv2.filter2D(img, -1, x_kernel)
abs_x = np.absolute(x_gradient)
x_grad_u8 = np.uint8(abs_x)
add_img(x_grad_u8, 'manual x gradient')

y_gradient = cv2.filter2D(img, -1, y_kernel)
abs_y = np.absolute(y_gradient)
y_grad_u8 = np.uint8(abs_y)
add_img(y_grad_u8, 'manual y gradient')


magnitude = cv2.magnitude(abs_x, abs_y)
magnitude_u8 = np.uint8(magnitude)
add_img(magnitude_u8, 'magnitude')
"""
lap = cv2.Laplacian(orig, -1, cv2.CV_64F)
add_img(np.uint8(lap), 'laplacian')
"""
canny = cv2.Canny(orig, 100, 200)
add_img(np.uint8(canny), 'Canny')

for i in range(len(images)):
    plt.subplot(1, len(images), i)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])

plt.show()
