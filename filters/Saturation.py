import numpy as np
from PIL import Image

def adjust_red_saturation(img_array, value):
    img_array = np.float32(img_array)
    img_array[:,:,0] += value
    img_array = np.clip(img_array, 0, 255)
    adjusted_image_array= img_array.astype(np.uint8)
    
    return adjusted_image_array

def adjust_green_saturation(img_array, value):
    img_array = np.float32(img_array)
    img_array[:,:,1] += value
    img_array = np.clip(img_array, 0, 255)
    adjusted_image_array= img_array.astype(np.uint8)
    
    return adjusted_image_array

def adjust_blue_saturation(img_array, value):
    img_array = np.float32(img_array)
    img_array[:,:,2] += value
    img_array = np.clip(img_array, 0, 255)
    adjusted_image_array= img_array.astype(np.uint8)
    
    return adjusted_image_array

