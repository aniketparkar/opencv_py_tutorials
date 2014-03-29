import cv2
import numpy as np

from cv2tutorial.util import fetch_image

img = fetch_image('messi5.jpg')
cv2.namedWindow('img')

pixel = img[100, 200]
print(pixel)

print(img.shape)

ball = img[280:340, 330:390]
img[273:333, 100:160] = ball
img[:,:,2] -= 5

cv2.namedWindow('img')

while(1):
    cv2.imshow('img', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
