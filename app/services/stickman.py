import base64

import cv2 
import numpy as np 
import PIL


class Stick:
    def __init__(self):
        self.img = []

    def get_image(self, pil_image):
        try:
            img = PIL.ImageChops.invert(pil_image)
            img = np.array(img)
            img = img[:, :, 1:]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.array((img > 233) * 255, np.uint8)
            
            self.img = img
            self.output = np.copy(self.img)
        except Exception as e:
            print(e)

    async def detect_head(self):
        edged = cv2.Canny(self.img, 30, 200) 
        contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in contours:
            x,y,w,h = cv2.boundingRect(contour)
            if abs(w - h) < 0.2 * h and abs(w - h) < 0.2 * w:
                break

        return x, y, w, h

    def add_eyes(self, head_cors):
        x, y, w, h = head_cors
        center = (int(x + w / 2), int(y + h / 2))
        left_eye = (int(center[0] - w / 4), int(center[1] - h / 6))
        right_eye = (int(center[0] + w / 4), int(center[1] - h / 6))
        cv2.circle(self.output, left_eye, int(w / 15), (0,0,0), -1)
        cv2.circle(self.output, right_eye, int(w / 15), (0,0,0), -1)

    def add_mouth(self, head_cors):
        x, y, w, h = head_cors
        center = (int(x + w / 2), int(y + h / 2))
        mouth_start = (int(center[0] - w / 3.5), int(center[1] + h / 4))
        mouth_end = (int(center[0] + w / 3.5), int(center[1] + h / 4))
        cv2.line(self.output, mouth_start, mouth_end, (0,0,0), 5)

    async def process(self):
        head_cors = await self.detect_head()
        self.add_eyes(head_cors)
        self.add_mouth(head_cors)