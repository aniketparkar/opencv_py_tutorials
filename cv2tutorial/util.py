import os.path

import cv2

def fetch_image(image_name, flags=-1):
    """Return an image from the images directory."""
    path = os.path.realpath(__file__)
    dirname = os.path.dirname(path)
    image_path = os.path.join(dirname, 'extra', 'images', image_name)
    image = cv2.imread(image_path, flags)
    return image
