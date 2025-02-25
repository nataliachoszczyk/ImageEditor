import numpy as np
from PIL import Image

class Negative:
    def __init__(self):
        pass
    def apply(self, image):
        """Apply negative filter to an image."""
        negative_image = 255 - image
        return negative_image