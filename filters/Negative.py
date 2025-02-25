import numpy as np
from PIL import Image

class Negative:
    def __init__(self):
        pass
    def apply(self, image):
        """Apply negative filter to an image."""
        img_array = np.array(image)
        negative_image = 255 - img_array
        return Image.fromarray(negative_image)