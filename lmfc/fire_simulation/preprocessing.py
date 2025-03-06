import numpy as np
from .indices import compute_ndvi, compute_ndmi, compute_nbr, compute_cwc

def extract_rgb_image(image):
    R, G, B = image[:, :, 3], image[:, :, 2], image[:, :, 1]
    RGB = np.dstack((R, G, B))
    return (RGB - RGB.min()) / (RGB.max() - RGB.min())

def get_image_features(image):
    return {
        'ndvi': compute_ndvi(image[:, :, 3], image[:, :, 7]),
        'ndmi': compute_ndmi(image[:, :, 7], image[:, :, 11]),
        'nbr': compute_nbr(image[:, :, 7], image[:, :, 12]),
        'cwc': compute_cwc(image[:, :, 8], image[:, :, 11]),
        'rgb': extract_rgb_image(image)
    }

def split_into_patches(image, patch_size=64):
    H, W, C = image.shape if len(image.shape) == 3 else (*image.shape, 1)
    H, W = H - (H % patch_size), W - (W % patch_size)
    image = image[:H, :W]
    patches = image.reshape(H // patch_size, patch_size, W // patch_size, patch_size, C)
    return patches.swapaxes(1, 2).reshape(-1, patch_size, patch_size, C)

