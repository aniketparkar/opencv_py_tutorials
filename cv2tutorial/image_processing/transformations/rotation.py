import cv2
import numpy as np

from cv2tutorial.util import fetch_image

def main():
    img = fetch_image('messi5.jpg', 0)
    rows,cols = img.shape

    M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))

    cv2.imshow('img', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
