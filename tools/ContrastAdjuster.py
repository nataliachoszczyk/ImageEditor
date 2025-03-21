import numpy as np

def adjust_contrast(img_array, factor):

    mean_intensity = img_array.mean(axis=(0, 1), keepdims=True)
    contrast_image = np.clip((img_array - mean_intensity) * factor + mean_intensity, 0, 255).astype(np.uint8)
    return contrast_image
