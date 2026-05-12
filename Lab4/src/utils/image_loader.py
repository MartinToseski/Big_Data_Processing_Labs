import numpy as np
from PIL import Image


def load_image_pixels(image_path, resize=None):
    img = Image.open(image_path).convert("RGB")

    if resize:
        img = img.resize(resize)

    image_array = np.array(img)
    pixels = image_array.reshape(-1, 3).astype(float)
    return pixels, image_array.shape