import numpy as np
from filters.Convolve import convolve

def sharpen(img_array, level):
    if level == 3: #mean-removal
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    elif level == 2: #hp1
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif level == 1: #hp2
        kernel = np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])

    img_array = np.float32(img_array)

    sharpened_img = np.zeros_like(img_array)

    for c in range(3):
        sharpened_img[..., c] = convolve(img_array[..., c], kernel)

    return np.clip(sharpened_img, 0, 255).astype(np.uint8)