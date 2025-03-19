import numpy as np
from tools.Convolve import convolve


def generate_box_kernel(kernel_size):
    return np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)

def generate_gaussian_kernel( kernel_size, sigma = 4):
    k = kernel_size // 2
    x, y = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return kernel / np.sum(kernel)

def generate_circular_kernel( kernel_size):
    k = kernel_size // 2
    y, x = np.ogrid[-k:k+1, -k:k+1]
    radius = k

    mask = x**2 + y**2 <= radius**2
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[mask] = 1

    kernel /= kernel.sum()
    return kernel


def blur(img_array, kernel_size, blur_type):
    if blur_type == "box":
        kernel = generate_box_kernel(kernel_size)
    elif blur_type == "gaussian":
        kernel = generate_gaussian_kernel(kernel_size)
    elif blur_type == "circular":
        kernel = generate_circular_kernel(kernel_size)
    img_array = np.float32(img_array)

    blurred_img = np.zeros_like(img_array)

    for c in range(3):
        blurred_img[..., c] = convolve(img_array[..., c], kernel)

    return np.clip(blurred_img, 0, 255).astype(np.uint8)