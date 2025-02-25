import numpy as np
from PIL import Image

class BrightAdjuster:
    def __init__(self):
        pass
    def adjust_brightness(self, value, image):
        adjusted_image_array = self.change_brightness(image, value)
        return adjusted_image_array

    def change_brightness(self, img_array, value):
        img_array = np.float32(img_array)
        img_array += value
        img_array = np.clip(img_array, 0, 255)
        return img_array.astype(np.uint8)
