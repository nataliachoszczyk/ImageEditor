import numpy as np

from tools.Convolve import convolve


def mask(img_array, kernel):
    kernel = np.array(kernel, dtype=np.float32)


    img_array = np.float32(img_array)
    res = np.zeros_like(img_array)

    for c in range(3):
        a = convolve(img_array[..., c], kernel)
        res[..., c] = a

    return np.clip(res, 0, 255).astype(np.uint8)