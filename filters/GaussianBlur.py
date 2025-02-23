import numpy as np
from PIL import Image

class GaussianBlur:
    def __init__(self):
        pass

    def generate_kernel(self, kernel_size, sigma):
        k = kernel_size // 2
        x, y = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
        kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        return kernel / np.sum(kernel)  # Normalize

    def apply(self, image,  kernel_size, sigma=1):
        """Applies Gaussian blur using convolution."""
        img_array = np.array(image.convert("RGB"), dtype=np.float32)
        kernel = self.generate_kernel(kernel_size, sigma)

        pad_size = kernel_size // 2
        padded_img = np.pad(img_array, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='reflect')

        blurred_img = np.zeros_like(img_array)

        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                for c in range(3):
                    region = padded_img[i:i + kernel_size, j:j + kernel_size, c]
                    blurred_img[i, j, c] = np.sum(region * kernel)

        return Image.fromarray(np.clip(blurred_img, 0, 255).astype(np.uint8))
