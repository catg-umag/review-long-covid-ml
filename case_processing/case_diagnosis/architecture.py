import tensorflow as tf
from tensorflow.keras.layers import *


class BaseModel(tf.keras.Model):
    def __init__(self, input_shape):
        super().__init__()

        self.C1 = Conv2D(32, (3 * 3), padding="same", input_shape=input_shape)
        self.B1 = BatchNormalization()
        self.A1 = Activation("relu")
        self.P1 = MaxPooling2D(2, padding="same")
        self.Dr1 = Dropout(0.3)

        self.C2 = Conv2D(32, (3 * 3), padding="same")
        self.B2 = BatchNormalization()
        self.A2 = Activation("relu")
        self.P2 = MaxPooling2D(2, padding="same")
        self.Dr2 = Dropout(0.3)

        self.C3 = Conv2D(32, (3 * 3), padding="same")
        self.B3 = BatchNormalization()
        self.A3 = Activation("relu")
        self.P3 = MaxPooling2D(2, padding="same")
        self.Dr3 = Dropout(0.3)

        self.F1 = Flatten()
        self.D1 = Dense(256, activation="relu")
        self.B4 = BatchNormalization()
        self.D2 = Dense(256, activation="relu")
        self.D3 = Dense(256, activation="relu")
        self.D4 = Dense(256, activation="relu")
        self.Dr3 = Dropout(0.3)
        self.D5 = Dense(1, activation="sigmoid")

    def call(self, x):
        x = self.C1(x)
        x = self.B1(x)
        x = self.A1(x)
        x = self.P1(x)
        x = self.Dr1(x)

        x = self.C2(x)
        x = self.B2(x)
        x = self.A2(x)
        x = self.P2(x)
        x = self.Dr1(x)

        x = self.C3(x)
        x = self.B3(x)
        x = self.A3(x)
        x = self.P3(x)
        x = self.Dr2(x)

        x = self.F1(x)
        x = self.D1(x)
        x = self.B4(x)
        x = self.D2(x)
        x = self.D3(x)
        x = self.D4(x)
        x = self.Dr3(x)
        y = self.D5(x)

        return y
