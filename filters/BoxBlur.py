import numpy as np
from PIL import Image
from scipy.signal import convolve2d

class BoxBlur:
    def __init__(self):
        pass

    def generate_kernel(self, kernel_size):
        """Generate a box blur kernel where all values are equal (mean filter)."""
        return np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)

    def apply(self, image, kernel_size):
        """Apply box blur using convolution."""
        img_array = np.array(image.convert("RGB"), dtype=np.float32)

        # Generate the uniform box blur kernel
        kernel = self.generate_kernel(kernel_size)

        # Apply the kernel to each color channel (R, G, B)
        blurred_img = np.zeros_like(img_array)

        for c in range(3):
            # Convolve the image with the box blur kernel
            blurred_img[..., c] = convolve2d(
                img_array[..., c], kernel, mode='same', boundary='symm'
            )

        # Clip the values to ensure they remain within valid range (0 to 255)
        return Image.fromarray(np.clip(blurred_img, 0, 255).astype(np.uint8))
