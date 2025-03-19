import numpy as np

def apply_grayscale(image, type):
    r, g, b = (.3, .59, .11) if type == "luminosity" else (.33, .33, .33)

    grayscale_values =(r * image[:, :, 0] +
                       g * image[:, :, 1] +
                       b * image[:, :, 2]).astype(np.uint8)

    grayscale_image = np.stack([grayscale_values] * 3, axis=-1)

    return grayscale_image