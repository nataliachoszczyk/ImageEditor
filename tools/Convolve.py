import numpy as np

def convolve(image, kernel):
    kernel_height, kernel_width = kernel.shape
    image_height, iw = image.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2

    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    output = np.zeros_like(image)

    for i in range(image_height):
        for j in range(iw):
            output[i, j] = np.sum(kernel * padded_image[i:i+kernel_height, j:j+kernel_width])

    return output