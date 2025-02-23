import numpy as np
from PIL import Image


class Grayscale:
    def __init__(self):
        self.original_image = None

    def apply(self, image, type):
        """Apply grayscale conversion using NumPy vectorized operations."""
        r, g, b = (.3, .59, .11) if type == "luminosity" else (.33, .33, .33)
        self.original_image = image.convert("RGB")
        img_array = np.array(self.original_image)

        grayscale_values =(r * img_array[:, :, 0] +
                           g * img_array[:, :, 1] +
                           b * img_array[:, :, 2]).astype(np.uint8)

        grayscale_image = np.stack([grayscale_values] * 3, axis=-1)

        return Image.fromarray(grayscale_image)