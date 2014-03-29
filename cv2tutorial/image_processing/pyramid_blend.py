import cv2
import numpy as np
from matplotlib import pyplot as plt

from cv2tutorial.util import fetch_image

images = []
titles = []

def add_img(image, title):
    global images, titles
    images.append(image)
    titles.append(title)


A = cv2.cvtColor(fetch_image('apple.jpg'), cv2.COLOR_BGR2RGB)
B = cv2.cvtColor(fetch_image('orange.jpg'), cv2.COLOR_BGR2RGB)

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpA.append(G)

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in xrange(6):
    G = cv2.pyrDown(G)
    gpB.append(G)

# generate Laplacian Pyramid for A
lpA = [gpA[5]]
for i in xrange(5,0,-1):
    GE = cv2.pyrUp(gpA[i])
    L = cv2.subtract(gpA[i-1],GE)
    lpA.append(L)

# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in xrange(5,0,-1):
    GE = cv2.pyrUp(gpB[i])
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)

# Now add left and right halves of images in each level
LS = []
for la,lb in zip(lpA,lpB):
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols/2], lb[:,cols/2:]))
    LS.append(ls)

# now reconstruct
ls_ = LS[0]
for i in xrange(1,6):
    ls_ = cv2.pyrUp(ls_)
    add_img(ls_, i)
    ls_ = cv2.add(ls_, LS[i])

# image with direct connecting each half
real = np.hstack((A[:,:cols/2],B[:,cols/2:]))

add_img(ls_, "pyramid")
#add_img(real, "stacked")

#for i in range(len(lpA)):
#    add_img(LS[i], i)


for i in range(len(images)):
    plt.subplot(1, len(images), i)
    plt.imshow(images[i])
    plt.title(titles[i])

plt.show()
