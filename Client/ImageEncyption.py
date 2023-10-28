import cv2
import numpy as np
from PIL import Image


def encrypt_image(path):
    image_input = cv2.imread(path, 0)
    (x, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1
    key = np.random.normal(mu, sigma, (x, y)) + np.finfo(float).eps

    enc_image = image_input / key
    cv2.imwrite(path, enc_image * 255)

    return key
