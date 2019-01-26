from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import configuration as conf
import numpy as np
from keras.models import model_from_json
from keras import optimizers

# System model
class Model:
    global model

    # optimizer pozmeneny
    global adam

    # Konstruktor
    def __init__(self):
        self.model = Sequential()
        self.adam = optimizers.Adam(lr=0.01)

    # Trenovanie
    def train(self, train_data, train_labels):
        res = self.model.fit(np.array(train_data), np.array(train_labels), batch_size=4, epochs=conf.EPOCH, verbose=1)
        self.save_model()
        return res

    # zlozenie modelu

    def model_summary(self):
        return self.model.summary()


    ##Vytvorenie modelu od podlahy
    def create_model(self):
        ## vstupna vrstva do modelu
        ## musi obsahovat vstupny shape, kvoli rozmeru v datach
        ## krnel size -- urcenie miesta kde sa vykkona v matik

        #odel.add(Flatten(input_shape=train_data.shape[1:]))

        self.model.add(Conv2D(32, kernel_size=(3, 3),  activation='relu',
                             padding='same', data_format='channels_last',
                              input_shape=(conf.IMG_SIZE_X,conf.IMG_SIZE_Y,3))) # pre obrazky s RGB treba 3
        self.model.add(MaxPooling2D(pool_size=(2, 2))) # zvyraznenie
        self.model.add(BatchNormalization())

        ## prvy filter
       # self.model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
        #self.model.add(Conv2D(64, (3, 3), activation='relu'))
        #self.model.add(MaxPooling2D(pool_size=(2, 2)))
        #self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        #self.model.add(Dense(10, activation='relu'))
        #self.model.add(BatchNormalization())

        ## vystupna vrstva

        self.model.add(Dense(1, activation='softmax'))

        self.model.compile(loss='binary_crossentropy', optimizer=self.adam, metrics=['accuracy'])



        return self.model

    # Nahranie uz vytvoreneho modelu
    def load_model(self):
        json_file = open('saved_model/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #nastavenie ulozenych vah
        loaded_model.load_weights("saved_model/model.h5")
        self.model.compile(loss='binary_crossentropy', optimizer=self.adam, metrics=['accuracy'])
        print("Loaded model from disk")

    # ulozenie modelu
    def save_model(self):
        json_model = self.model.to_json()
        with open("saved_model/model.json", "w") as json_file:
            json_file.write(json_model)
        #ulozenie vah
        self.model.save_weights("saved_model/model.h5")
        print("Saved model to disk")

    # Model evaulation
    def test_model(self,test_data,test_labels):
        print('Model evaulation(Test set used):')
        result = self.model.evaluate(test_data, test_labels, batch_size=4)
        print('Evaulation completed:')
        i = 0
        for score in result:
            print('Name:{} Value:{}'.format(self.model.metrics_names[i], score))
            i += 1
        print('=========================')

    # predikuje pre jeden obrazok
    # pre mnozinu EX-ANTE
    def predict_image(self,img):
        predicted = self.model.predict(img,batch_size=None,verbose=0,steps=None)
        return predicted

    # generuje predikcie pre celu mnozinu
    # generuje ich pre mnozinu so znamou hodnotou
    # len pre EX-POST alebo nejaky batch vacsi
    def model_generated_predictions(self, data, labels):
        result = self.model.predict(data)
        # , abs(result - labels)
        return result