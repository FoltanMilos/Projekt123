from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import numpy as np
from keras.models import model_from_json
from keras import optimizers
from sklearn.metrics import classification_report
import config as conf
import interface.model_interface as interface
import neural_nets.cnn.callbacks as CallBack
import keras.initializers
from keras.preprocessing.image import ImageDataGenerator
import neural_nets.cnn.results_set as ResultSet

# System model
class Model_cnn(interface.ModelInterface):
    global model

    # optimizer pozmeneny
    global adam

    #referencia na data patriace modelu
    global ref_data

    #resulty modelu
    global result_processing

    # Konstruktor
    def __init__(self,ref_data):
        self.result_processing =  ResultSet.Results_set(self)
        self.model = Sequential()
        #self.adam = optimizers.Adam(lr=conf.learning_coef)
        #self.initializer = keras.initializers.TruncatedNormal(mean=0.0, stddev=0.05, seed=conf.initializer_seed)
        self.initializer = keras.initializers.glorot_uniform(conf.initializer_seed)
        self.bias_initializer = keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
        self.ref_data = ref_data
        self.adam = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
        #self.adam = keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
        self.train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

        # Trenovanie
    def train(self, train_set, valid_set):
        #res = self.model.fit(np.array(train_data), np.array(train_labels)[:,0], batch_size=11, epochs=conf.EPOCH, verbose=1,
        #                     callbacks=[CallBack.Callback_after_epoch(np.array(self.ref_app.data.test_data),
        #                                                              np.array(self.ref_app.data.test_labels)[:,0],self)],
        #                     validation_data=(np.array(self.ref_data.test_data),np.array(self.ref_app.data.test_labels)[:,0]))
        res = self.model.fit_generator(
            train_set ,steps_per_epoch=250,epochs=conf.EPOCH,
            validation_data=valid_set,
            validation_steps=100,
            callbacks = [EarlyStopping(monitor='val_acc',
                                       patience=200,
                                       verbose=1)]),
                         #TensorBoard(log_dir='./logs',histogram_freq=0,batch_size=32,write_graph=True,write_images=False)])
        #TODO: niekto kto si dufa by mohol spravit callback na tensorflow board
        # cmd tensorboard --logdir=/full_path_to_your_logs
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
                              activation='relu',
                              padding='valid',
                              bias_initializer=self.bias_initializer,
                              input_shape=(conf.IMG_SIZE_X,conf.IMG_SIZE_Y,3),
                              kernel_initializer=self.initializer)
                       )
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        # 2. VRSTVA
        self.model.add(Conv2D(32,
                              (3, 3),
                              padding='valid'))
        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())  # normalizuje na 0 - 1

        # 3.VRSTVA
        self.model.add(Conv2D(16,
                              (3, 3),
                              padding='valid',
                              activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())

        # FULL CONNECTED -tu pride asi viacej vrstiev
        self.model.add(Dense(64, activation='sigmoid'))
        self.model.add(Dense(128, activation='sigmoid'))

        # predvystupna - aby sa dali nadpojit vystupy
        self.model.add(Dense(10, activation='sigmoid'))

        # VYSTUPNA VRSTVA -sigmoid - vraj to ma byt ale nie som s tym stotozneny
        self.model.add(Dense(1, activation='sigmoid'))

        # compilovanie rmsprop ??mean_squared_error, rmsprop ?? najlepsie
        self.model.compile(loss="binary_crossentropy",
                           optimizer='adadelta',
                           metrics=['accuracy'])
        return self.model

    # Nahranie uz vytvoreneho modelu
    def load_model(self):
        json_file = open('saved_model/cnn/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        #nastavenie ulozenych vah
        loaded_model.load_weights("saved_model/cnn/model.h5")
        self.model.compile(loss='binary_crossentropy', optimizer='adadelta', metrics=['accuracy'])
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
    def test_model(self):
        print('Model evaulation(Test set used):')
        #result = self.model.evaluate(np.array(test_data), np.array(test_labels)[:,0], batch_size=1)
        result = self.model.evaluate_generator(self.ref_data.load_test_set())
        print('Evaluation completed:')
        i = 0
        for score in result:
            print('Name:{} Value:{}'.format(self.model.metrics_names[i], score))
            i += 1
        print('=========================')
        return result[0],result[1]

    def predict_image(self,image=None):
        """Predikcia jedneho obrazku"""
        if(image is None):
            raise Exception("Error by predict image. Image is None!")
        image = self.ref_data.preproces_image(image)
        predicted = self.model.predict(image,batch_size=1,verbose=0,steps=1)
        return predicted


    def predict_image_flow(self):
        image_exante_set =  self.ref_data.load_image_exante_flow()
        #image_exante_set.reset()
        result_set = self.model.predict_generator(image_exante_set,
                                                  steps=len(image_exante_set.filenames),
                                                  verbose=0)
        res_string = self.result_processing.process_results(result_set,
                                                     np.array(image_exante_set.classes).reshape(len(image_exante_set.classes),1)
                                                     ,image_exante_set.filenames)
        return res_string