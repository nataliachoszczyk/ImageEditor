import numpy as np
from scipy.signal import convolve2d


def sharpen(img_array, level):
    if level == 3: #mean-removal
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    elif level == 2: #hp1
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif level == 1: #hp2
        kernel = np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])


    img_array = np.float32(img_array)
    height, width = img_array.shape[:2]
    # if height > 1000 or width > 1000:
    #     kernel_size = max(3, kernel_size // 2)  # Reduce kernel size for large images

    sharpened_img = np.zeros_like(img_array)

    for c in range(3):
        sharpened_img[..., c] = convolve2d(
            img_array[..., c], kernel, mode='same', boundary='symm'
        )

    return np.clip(sharpened_img, 0, 255).astype(np.uint8)