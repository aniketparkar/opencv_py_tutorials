from matplotlib import pyplot as plt

class Displayer(object):
    """"Display a group of images."""

    def __init__(self):
        self.images = []
        self.titles = []

    def add_image(self, image, title):
        self.images.append(image)
        self.titles.append(title)

    def display(self, cmap=None):
        for i in range(len(self.images)):
            plt.subplot(1, len(self.images), i)
            plt.imshow(self.images[i], cmap)
            plt.title(self.titles[i])

        plt.show()
