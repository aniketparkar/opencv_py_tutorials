import cv2
import numpy as np
from matplotlib import pyplot as plt

from cv2tutorial.util import fetch_image

def main():
    img = fetch_image('drawing.png')
    rows,cols,ch = img.shape


    pts1 = np.float32([[50,50], [200,50], [50, 200]])
    pts2 = np.float32([[10,100], [100, 50], [100, 250]])

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()

if __name__ == '__main__':
    main()
