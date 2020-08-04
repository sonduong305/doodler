import os

import cv2
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.metrics import categorical_accuracy, top_k_categorical_accuracy, categorical_crossentropy

from core.errors import PredictException, ModelLoadException
from core.config import MODEL_NAME, MODEL_PATH


class DoodlerMobileNet:
    def __init__(self):
        self.size = 64
        self.model = MobileNet(input_shape=(
            self.size, self.size, 1), alpha=1., weights=None, classes=340)

        self.model.compile(optimizer=Adam(lr=0.002), loss='categorical_crossentropy',
                           metrics=[categorical_crossentropy, categorical_accuracy])

    def warm_up(self):
        dummy_input = np.ones((1, 64, 64, 1))
        self.model.predict(dummy_input, batch_size=1)

    def load_model(self):
        if MODEL_PATH.endswith("/"):
            model_path = f'{MODEL_PATH}{MODEL_NAME}'
            labels_path = f'{MODEL_PATH}labels.txt'
        else:
            model_path = f'{MODEL_PATH}/{MODEL_NAME}'
            labels_path = f'{MODEL_PATH}/labels.txt'

        if not os.path.exists(model_path):
            message = f'Machine learning model at {model_path} does not exists!'
            logger.error(message)
            raise FileNotFoundError(message)

        with open(labels_path) as f:
            self.labels = f.read().splitlines()

        self.model.load_weights(model_path)

    def predict(self, img):
        print('image shape ', img.shape)
        input = cv2.resize(img, (self.size, self.size))
        input = cv2.GaussianBlur(input, (3, 3), 0)

        input = input[:, :, None]
        input = np.array((-input / 255) * 2) - 1
        input = input[None, :, :, :]

        output = self.model.predict(input, batch_size=1)[0]

        result = self.labels[np.argmax(output)]
        confident = np.max(output)

        return result, confident


model = DoodlerMobileNet()
