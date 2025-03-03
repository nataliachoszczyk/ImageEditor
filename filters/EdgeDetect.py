import numpy as np
from filters.convolve import convolve

def roberts_cross(img_array):
    kernel_a = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_b = np.array([[0, 1], [-1, 0]], dtype=np.float32)

    img_array = np.float32(img_array)
    res = np.zeros_like(img_array)

    for c in range(3):
        a = convolve(img_array[..., c], kernel_a)
        b = convolve(img_array[..., c], kernel_b)
        res[..., c] = np.sqrt(a**2 + b**2)

    return np.clip(res, 0, 255).astype(np.uint8)

def sobel_operator(img_array):
    kernel_a = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=np.float32)
    kernel_b = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32)

    img_array = np.float32(img_array)
    res = np.zeros_like(img_array)

    for c in range(3):
        a = convolve(img_array[..., c], kernel_a)
        b = convolve(img_array[..., c], kernel_b)
        res[..., c] = np.sqrt(a**2 + b**2)

    return np.clip(res, 0, 255).astype(np.uint8)

def laplace_filter(img_array):
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32)

    img_array = np.float32(img_array)
    res = np.zeros_like(img_array)

    for c in range(3):
        res[..., c] = convolve(img_array[..., c], kernel)

    return np.clip(res, 0, 255).astype(np.uint8)