import numpy as np
from PIL import Image

def apply_threshold( image, threshold):

    intensity = image.sum(axis=-1)

    binary_image = np.stack([np.where(intensity < threshold*3, 0, 255).astype(np.uint8)] * 3, axis=-1)

    return binary_image
