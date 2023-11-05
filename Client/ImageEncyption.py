import cv2
import numpy as np
from PIL import Image


def encrypt_image(path):
    image_input = cv2.imread(path, 0)
    (x, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1
    username = 'name'
    key = 1
    for letter in username:
        key *= ord(letter)

    enc_image = image_input / key
    cv2.imwrite(path, enc_image)

    return key


def decrypt_image(path, key):
    image_output = cv2.imread(path, 0)
    image_output *= key
    cv2.imwrite('image_output.jpg', image_output)


path = "C:/Users/liram/CyberFaceDetection/Faces/omer.jpeg"
key = encrypt_image(path)
print(key)
decrypt_image(path, key)
