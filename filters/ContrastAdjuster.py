import numpy as np
from PIL import Image

def adjust_contrast(img_array, factor):

    mean_intensity = img_array.mean(axis=(0, 1), keepdims=True)

    # Apply contrast adjustment (factor > 1 increases, factor < 1 decreases)
    contrast_image = np.clip((img_array - mean_intensity) * factor + mean_intensity, 0, 255).astype(np.uint8)

    return contrast_image
