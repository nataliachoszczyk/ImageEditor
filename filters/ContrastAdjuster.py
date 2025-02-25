import numpy as np
from PIL import Image


class ContrastAdjuster:
    def __init__(self):
        self.original_image = None

    def apply(self, image, factor):
        """Apply contrast adjustment to an image:
        factor > 1 increases contrast, factor < 1 decreases contrast."""
        self.original_image = image.convert("RGB")
        img_array = np.array(self.original_image)

        # Calculate the mean color value of the image to serve as a reference
        mean_intensity = img_array.mean(axis=(0, 1), keepdims=True)

        # Apply contrast adjustment (factor > 1 increases, factor < 1 decreases)
        contrast_image = np.clip((img_array - mean_intensity) * factor + mean_intensity, 0, 255).astype(np.uint8)

        return Image.fromarray(contrast_image)
