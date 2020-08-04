import base64
import io

import numpy as np
import cv2
import PIL
from PIL import Image


# Take in base64 string and return numpy image
def string_to_image(base64_string):
    imgdata = base64.urlsafe_b64decode(base64_string)
    pil_image = Image.open(io.BytesIO(imgdata))
    img = PIL.ImageChops.invert(pil_image)
    img = np.array(img)
    img = img[:, :, 1:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.array((img > 233) * 255, np.uint8)

    return img
