import numpy as np
from PIL import Image


def apply_negative(image):
    negative_image = 255 - image
    return negative_image