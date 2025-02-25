import numpy as np
from PIL import Image

class Threshold:
    def __init__(self):
        pass

    def apply(self, image, threshold):
        """Apply thresholding to an image: Pixels below threshold become black, others white."""


        intensity = image.sum(axis=-1)

        binary_image = np.stack([np.where(intensity < threshold*3, 0, 255).astype(np.uint8)] * 3, axis=-1)

        return binary_image
