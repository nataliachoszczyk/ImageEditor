import numpy as np

def convolve(image, kernel):
    kh, kw = kernel.shape
    ih, iw = image.shape
    pad_h, pad_w = kh // 2, kw // 2

    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    output = np.zeros_like(image)

    for i in range(ih):
        for j in range(iw):
            output[i, j] = np.sum(kernel * padded_image[i:i+kh, j:j+kw])

    return output