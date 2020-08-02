import base64 
import io

from PIL import Image


# Take in base64 string and return PIL image
def string_to_image(base64_string):
    imgdata = base64.urlsafe_b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))