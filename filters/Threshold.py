import numpy as np
from PIL import Image

class Threshold:
    def __init__(self):
        self.original_image = None

    def apply(self, image, threshold):
        """Apply thresholding to an image: Pixels below threshold become black, others white."""
        self.original_image = image.convert("RGB")
        img_array = np.array(self.original_image)

        intensity = img_array.sum(axis=-1)

        binary_image = np.stack([np.where(intensity < threshold*3, 0, 255).astype(np.uint8)] * 3, axis=-1)

        return Image.fromarray(binary_image)
