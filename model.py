import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers. normalization import BatchNormalization
import numpy as np
import configuration as conf


# System model
class Model:
    global model

    def __init__(self):
        pass

    def train(self, train_data, train_labels):
        self.model.fit(train_data, train_labels, batch_size=2, epochs=conf.EPOCH, verbose=1)

    def predict(self):
        pass


    ##Vytvorenie modelu od podlady
    def create_model(self):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y, 3)))
        self.model.add(Conv2D(32, (3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return self.model

    ##Nahranie uz vytvoreneho modelu
    def load_model(self):
        pass


    def save_model(self):
        json_model = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(json_model)

    def predict_image(self,img):
        predicted = self.model.predict(img,batch_size=None,verbose=0,steps=None)
        return predicted