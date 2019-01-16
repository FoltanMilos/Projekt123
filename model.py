from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import configuration as conf
import numpy as np
from keras.models import model_from_json

# System model
class Model:
    global model

    def __init__(self):
        pass

    def train(self, train_data, train_labels):
        self.model.fit(np.array(train_data), np.array(train_labels), batch_size=3, epochs=conf.EPOCH, verbose=1)
        self.save_model()

    def predict(self):
        pass


    ##Vytvorenie modelu od podlady
    def create_model(self):
        self.model = Sequential()
        ##VSTUPNA VRSTVA
        self.model.add(Conv2D(32, (3, 3),  activation='relu',
                             padding='same', data_format='channels_last', input_shape=(conf.IMG_SIZE_X,conf.IMG_SIZE_Y,3))) ##pre obrazky s RGB

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())

        self.model.add(Dense(1, activation='softmax'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return self.model

    ##Nahranie uz vytvoreneho modelu
    def load_model(self):
        json_file = open('saved_model/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #nastavenie ulozenych vah
        loaded_model.load_weights("saved_model/model.h5")
        print("Loaded model from disk")


    def save_model(self):
        json_model = self.model.to_json()
        with open("saved_model/model.json", "w") as json_file:
            json_file.write(json_model)
        #ulozenie vah
        model.save_weights("saved_model/model.h5")
        print("Saved model to disk")


    def predict_image(self,img):
        predicted = self.model.predict(img,batch_size=None,verbose=0,steps=None)
        return predicted