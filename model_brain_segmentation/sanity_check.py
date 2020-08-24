import base64
import os
import requests
import json
from PIL import Image
from io import BytesIO
from skimage.io import imsave
import cv2
import numpy as np
from inference import Segmentation

samples = "./samples/"

segm = Segmentation()

for subdir, dirs, files in os.walk(samples):
    for f in files:
        path = subdir + f
        print(path)

        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        output = segm.ask(encoded_string)
        output = BytesIO(output)
        img = Image.open(output)

        img.save(os.path.join(subdir, f"result_{f}"), "PNG")
