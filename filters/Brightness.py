import numpy as np
from PIL import Image

def adjust_brightness(image, value):
    def change_brightness(img_array, value):
        img_array = np.float32(img_array)
        img_array += value
        img_array = np.clip(img_array, 0, 255)
        return img_array.astype(np.uint8)

    adjusted_image_array = change_brightness(image, value)
    return adjusted_image_array


