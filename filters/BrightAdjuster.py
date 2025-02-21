import numpy as np
from PIL import Image

class BrightAdjuster:
    def __init__(self, image):
        self.original_image = image.convert("RGB")

    def adjust_brightness(self, value):
        img_array = np.array(self.original_image)
        adjusted_image_array = self.change_brightness(img_array, value)
        return Image.fromarray(adjusted_image_array)

    def change_brightness(self, img_array, value):
        img_array = img_array.astype(np.float32)
        img_array += value
        img_array = np.clip(img_array, 0, 255)
        return img_array.astype(np.uint8)
