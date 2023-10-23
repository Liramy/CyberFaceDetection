import base64

import face_recognition
import tenseal as ts
import os, sys
import cv2
import numpy as np
import math

from Face_Recognition import FaceRecognition

# Explanation about the type of code needed -
# https://sefiks.com/2021/12/01/homomorphic-facial-recognition-with-tenseal/

context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.generate_galois_keys()
context.global_scale = 2 ** 40


def write_data(file_name, data):
    if type(data) == bytes:
        # bytes to base64
        data = base64.b64encode(data)

    with open(file_name, 'wb') as f:
        f.write(data)


def read_data(file_name):
    with open(file_name, "rb") as f:
        data = f.read()
    # base64 to bytes
    return base64.b64decode(data)


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
