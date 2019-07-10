from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import numpy as np
from keras.models import model_from_json
from keras import optimizers
import config as conf
import interface.model_interface as interface
import neural_nets.cnn.callback_after_epoch as CallBack
import keras.initializers

# System model
class Model_cnn(interface.ModelInterface):
    global model

    # optimizer pozmeneny
    global adam

    # Konstruktor
    def __init__(self,ref_app):
        self.model = Sequential()
        #self.adam = optimizers.Adam(lr=conf.learning_coef)
        #self.initializer = keras.initializers.TruncatedNormal(mean=0.0, stddev=0.05, seed=conf.initializer_seed)
        self.initializer = keras.initializers.glorot_uniform(conf.initializer_seed)
        self.bias_initializer = keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
        self.ref_app = ref_app
        self.adam = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
        #self.adam = keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)

        # Trenovanie
    def train(self, train_data, train_labels):
        res = self.model.fit(np.array(train_data), np.array(train_labels)[:,0], batch_size=2, epochs=conf.EPOCH, verbose=1,
                             callbacks=[CallBack.Callback_after_epoch(np.array(self.ref_app.data.test_data),
                                                                      np.array(self.ref_app.data.test_labels)[:,0],self)],
                             validation_data=(np.array(self.ref_app.data.test_data),np.array(self.ref_app.data.test_labels)[:,0]))
        self.save_model()
        return res

    # zlozenie modelu
    def model_summary(self):
        return self.model.summary()

    ##Vytvorenie modelu od podlahy
    def create_model(self):
        # VSTUPNA
        self.model.add(Conv2D(64,
                              kernel_size=3,
                              #activation='relu',
                              padding='valid',
                              bias_initializer=self.bias_initializer,
                              input_shape=(conf.IMG_SIZE_X,conf.IMG_SIZE_Y,3),
                              kernel_initializer=self.initializer)
                       )
        self.model.add(Conv2D(32, (3, 3), padding='same')) #, activation='relu')
        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())  # normalizuje na 0 - 1

        self.model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))

        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        #self.model.add(Dropout(0.5))  # reduces overfit

        self.model.add(Dense(64, activation='sigmoid'))
        self.model.add(Dense(128, activation='sigmoid'))
        self.model.add(Dense(64, activation='sigmoid'))
        ## 2.VRSTVA

        #self.model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
        #self.model.add(MaxPooling2D(pool_size=(2, 2)))

        #self.model.add(Dropout(0.5))
        ## vystupna vrstva
        self.model.add(Dense(1, activation='softmax'))

        # compilovanie mean_absolute_percentage_error
        self.model.compile(loss='mean_squared_error', optimizer=self.adam, metrics=['accuracy'])
        return self.model

    # Nahranie uz vytvoreneho modelu
    def load_model(self):
        json_file = open('saved_model/cnn/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #nastavenie ulozenych vah
        loaded_model.load_weights("saved_model/cnn/model.h5")
        self.model.compile(loss='binary_crossentropy', optimizer=self.adam, metrics=['accuracy'])
        print("Loaded model from disk")

    # ulozenie modelu
    def save_model(self):
        json_model = self.model.to_json()
        with open("saved_model/cnn/model.json", "w") as json_file:
            json_file.write(json_model)
        #ulozenie vah
        self.model.save_weights("saved_model/cnn/model.h5")
        print("Saved model to disk")

    # Model evaluation
    def test_model(self,test_data,test_labels):
        print('Model evaulation(Test set used):')
        result = self.model.evaluate(np.array(test_data), np.array(test_labels)[:,0], batch_size=1)
        print('Evaluation completed:')
        i = 0
        for score in result:
            print('Name:{} Value:{}'.format(self.model.metrics_names[i], score))
            i += 1
        print('=========================')
        return result[0],result[1]

    # predikuje pre jeden obrazok
    # pre mnozinu EX-ANTE
    def predict_image(self,img):
        img = np.array(img) # img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS)
        img = np.expand_dims(img,axis=0)
        predicted = self.model.predict(img,batch_size=None,verbose=0,steps=None) #
        return predicted

    # generuje predikcie pre celu mnozinu
    # generuje ich pre mnozinu so znamou hodnotou
    # len pre EX-POST alebo nejaky batch vacsi
    def model_generated_predictions(self, data, labels):
        data = np.array(data)
        dataset = np.expand_dims(data, axis=0)
        result = self.model.predict(dataset)
        # , abs(result - labels)
        return result

    ## toto tu ani netreba
    ## hodnoty v evaulate su dobre
    def validate_model_on_test_data(self,data,labels):
        labels = np.array(labels)
        result = self.model.predict(np.array(data))
        i = 0
        ok = 0
        for lab in labels:
            if(int(lab[0]) == int(result[i])):
                ok+=1
            print("Result NN: {}  - label: {}  - name Pic: {} ".format(result[i],lab[0],lab[1]))
            i+=1
        print("Accuracy test set: {}%".format((ok/len(labels))*100))

