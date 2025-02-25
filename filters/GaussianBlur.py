import numpy as np
from PIL import Image
from scipy.signal import convolve2d

class GaussianBlur:
    def __init__(self):
        pass

    def generate_kernel(self, kernel_size, sigma):
        """Generate a Gaussian kernel."""
        k = kernel_size // 2
        x, y = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))
        kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        return kernel / np.sum(kernel)  # Normalize to make sure the sum is 1

    def apply(self, image, kernel_size, sigma=5):
        """Apply Gaussian blur using convolution."""
        img_array = np.array(image.convert("RGB"), dtype=np.float32)

        # Generate the Gaussian kernel
        kernel = self.generate_kernel(kernel_size, sigma)

        # Adjust kernel size for larger images (optional for performance)
        height, width = img_array.shape[:2]
        if height > 1000 or width > 1000:
            kernel_size = max(3, kernel_size // 2)  # Reduce kernel size for large images

        # Apply the kernel to each color channel (R, G, B)
        blurred_img = np.zeros_like(img_array)

        for c in range(3):
            # Convolve the image with the Gaussian kernel for each color channel
            blurred_img[..., c] = convolve2d(
                img_array[..., c], kernel, mode='same', boundary='symm'
            )

        # Clip the values to ensure they remain within valid range (0 to 255)
        return Image.fromarray(np.clip(blurred_img, 0, 255).astype(np.uint8))

