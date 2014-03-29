#!/usr/bin/env python
import cv2
import numpy as np

from cv2tutorial.util import fetch_image

img = fetch_image('messi5.jpg')

res = cv2.resize(img, None, fx=3, fy=2, interpolation=cv2.INTER_CUBIC)

cv2.imshow('img', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
