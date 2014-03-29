import cv2
import numpy as np
from matplotlib import pyplot as plt

from cv2tutorial.util import fetch_image

def main():
    img = fetch_image('sudokusmall.png')
    rows,cols,ch = img.shape

    pts1 = np.float32([[56,65],[68,52],[28,387],[389,390]])
    pts2 = np.float32([[0,0],[40,0],[0,300],[300,300]])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(300,300))

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    plt.show()

if __name__ == '__main__':
    main()
