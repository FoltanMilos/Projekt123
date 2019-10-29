from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import numpy as np
from keras.models import model_from_json
import src.config as conf
import src.interface.model_interface as interface
import keras.initializers
import src.models.cnn.results_set as ResultSet
import os
import json
import src.enum.enum_model_builder as mb
import src.data as dt
import random


class Model_cnn(interface.ModelInterface):
    global model  # instancia modelu keras
    global name  # nazov modelu
    global m_id  # model id
    global ref_data  # referencia na data patriace modelu
    global ref_res_proc  # referencia na vysledky
    global ref_app
    # resulty modlu
    global result_processing
    global ref_user  # referencia na uzivatela, ktoremu model patri
    global is_new  # ci je novo vytvoreny model
    global is_changed  # ci bola zmenena

    def __init__(self, model_name, ref_user, ref_app, ref_data=None):
        # povinne parametre
        self.ref_user = ref_user
        self.ref_app = ref_app
        if model_name == "":
            # prazdna instania, do ktorej sa naloaduju data
            self.is_new = False
            self.is_changed = False
        else:
            # instancia, ktora bola nanovo vytvorena. Pozor, vypyta si naspat ID z db, podla neho sa vytvaraju priecinky
            self.ref_data = ref_data
            self.is_new = True
            self.is_changed = False
            self.name = model_name
            self.ref_res_proc = ResultSet.Results_set(self, True)
            # self.ref_res_proc.save_state()
            self.path_struct = None
            self.path_weights = None
            self.model = Sequential()
            self.optimizer = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
            # ADADELTA --> an adaptive learning rate method
            #  Adadelta is a more robust extension of Adagrad that adapts learning rates based on a moving window of gradient updates,
            #  instead of accumulating all past gradients. This way, Adadelta continues learning even when many updates have been done.
            #  Compared to Adagrad, in the original version of Adadelta you don't have to set an initial learning rate. In this version,
            #  initial learning rate and decay factor can be set, as in most other Keras optimizers.
            self.initializer = keras.initializers.glorot_uniform(conf.initializer_seed)
            self.bias_initializer = keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
            self.save_state()

    # Ulozenie historie trenovania
    def save_train_history(self, train_history):
        hist_path = 'saved_model/cnn/' + str(int(self.m_id)) + '/training_session.txt'
        f = open(hist_path, "w")
        f.write(train_history)
        print("Training history has been saved.")
        f.close()

    # Trenovanie
    def train(self):
        if (self.ref_data != None):
            self.ref_data.load_train_set()
            self.ref_data.load_validation_set()
        else:
            raise Exception("No instance DATA has been picked for training")
        res = self.model.fit_generator(
            self.ref_data.train_set, steps_per_epoch=10, epochs=5,
            validation_data=self.ref_data.valid_set,
            validation_steps=5,
            callbacks=[EarlyStopping(monitor='acc',
                                     patience=200,
                                     verbose=1)]),
        self.is_changed = True
        self.path_struct = 'saved_model/cnn/' + str(int(self.m_id)) + '/model.json'
        self.path_weights = 'saved_model/cnn/' + str(int(self.m_id)) + '/model.h5'
        self.save()
        self.is_new = False
        self.save_state()
        return res

    # zlozenie modelu
    def summary(self):
        return self.model.summary()

    # Vytvorenie modelu od podlahy
    def create(self):
        # VSTUPNA
        self.model.add(Conv2D(64,
                              kernel_size=3,
                              activation='relu',
                              padding='valid',
                              bias_initializer=self.bias_initializer,
                              input_shape=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y, 3),
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

        # compilovanie rmsprop ??mean_squared_error, rmsprop ?? najlepsie bola adadelta
        self.model.compile(loss="binary_crossentropy",
                           optimizer=self.optimizer,
                           metrics=['accuracy'])
        return self.model

    # Nahranie uz vytvoreneho modelu
    def load(self):
        # tf.global_variables_initializer()
        json_file = open(self.path_struct, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # nastavenie ulozenych vah
        self.model.load_weights(self.path_weights)
        self.model.compile(loss='binary_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        self.model._make_predict_function()
        print("Loaded model from disk")

    # ulozenie modelu
    def save(self):
        json_model = self.model.to_json()
        with open(self.path_struct, "w+") as json_file:
            json_file.write(json_model)
        # ulozenie vah
        self.model.save_weights(self.path_weights)
        # self.test()
        print("Saved model to disk")

    # Model evaluation
    def test(self):
        print('Model evaulation(Test set used):')
        # result = self.model.evaluate(np.array(test_data), np.array(test_labels)[:,0], batch_size=1)
        result = self.model.evaluate_generator(self.ref_data.load_test_set())
        print('Evaluation completed:')
        i = 0
        for score in result:
            print('Name:{} Value:{}'.format(self.model.metrics_names[i], score))
            i += 1
        print('=========================')
        return result[0], result[1]

    def predict_image(self, image=None):
        """Predikcia jedneho obrazku"""
        if (image is None):
            raise Exception("Error by predict image. Image is None!")
        image = self.ref_data.preproces_image(image)
        predicted = self.model.predict(image)
        return predicted

    # TODO: na predikciu dakeho vaciseho sbor
    def predict_image_flow(self):
        image_exante_set = self.ref_data.load_image_exante_flow(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\validation\\')
        image_exante_set.reset()
        result_set = self.model.predict_generator(image_exante_set,
                                                  steps=len(image_exante_set.filenames),
                                                  verbose=0)
        res_string = self.result_processing.process_results(result_set,
                                                            np.array(image_exante_set.classes).reshape(
                                                                len(image_exante_set.classes), 1)
                                                            , image_exante_set.filenames)
        return res_string

    def load_state(self, state):
        self.m_id = int(state[0])
        self.path_struct = state[6]
        self.path_weights = state[5]
        self.is_new = False
        self.name = state[7]
        self.locked_by_training = state[8]
        self.trained_on_dataset = state[9]
        self.static = state[10]

        # dotiahnutie dat
        self.ref_data = dt.Data(self)
        self.ref_data.load_state()

        # dotiahnutie resutov
        self.ref_res_proc = ResultSet.Results_set(self, False)
        self.ref_res_proc.load_state()

        # nacitanie modelu
        self.load()

    def save_state(self):
        if self.is_new:
            # najprv result_set
            self.ref_res_proc.save_state()
            # insert
            self.m_id = self.ref_app.ref_db.insert_returning_identity(
                "insert into proj_model(u_id,r_id,m_type,m_weights_path,m_structure_path,model_name) values"
                "(" + str(self.ref_user.u_id) + ", " + str(
                    self.ref_res_proc.r_id) + ",'CNN'" + ",'" + "','" + "','" + str(self.name) + "')"
                , "m_id")
            # ak je novy model, treba  u vytvorit este aj folder
            os.mkdir(os.getcwd() + '/saved_model/cnn/' + str(int(self.m_id)))
            self.ref_app.ref_db.commit()

        if self.is_changed and self.is_new == False:
            self.ref_app.ref_db.update_statement(
                "update proj_model set r_id=" + str(self.ref_res_proc.r_id) + ", m_weights_path='" + str(
                    self.path_weights) +
                "', m_structure_path='" + str(self.path_struct) + "', model_name='" + str(
                    self.name) + "' where m_id=" + str(self.m_id))
            self.ref_app.ref_db.commit()

    def model_to_json(self):
        ret_json = {}
        headers = {}
        layers = []

        #hlavicka modelu
        headers["Name"] = self.name
        headers["Accuracy"] = random.randint(1,100) / 100.0

        # z datasetu
        dataset_json = None
        if self.trained_on_dataset is not None:
            dataset_json = self.ref_data.to_json()

        # VRSTVY
        ret_json["model_header"] = headers
        ret_json["data_header"] = dataset_json
        ret_json["layers"] = layers


        return ret_json



    def create_model_from_json(self, p_json):
        for lay in p_json["layers"]:
            if lay["NAME"] == mb.EnumLayer.INPUT.value:
                self.model.add(Conv2D(int(lay["count"]),
                                      kernel_size=int(lay["kernel_size"]),
                                      activation=str(lay["activation"]),
                                      padding=str(lay["padding"]),
                                      input_shape=(int(str(lay["input_shape"]).split('x')[0]),
                                                   int(str(lay["input_shape"]).split('x')[1]),
                                                   3)
                                      )
                               )
            elif lay["NAME"] == mb.EnumLayer.FLATTENING.value:
                self.model.add(Flatten())
            elif lay["NAME"] == mb.EnumLayer.POOLING.value:
                self.model.add(MaxPooling2D(pool_size=(int(str(lay["pool size"])),
                                                       int(str(lay["pool size"]))))
                               )
            elif lay["NAME"] == mb.EnumLayer.DENSE.value:
                self.model.add(Dense(int(str(lay["neuron_count"]))
                                     , activation=str(lay["activation"])))
            elif lay["NAME"] == mb.EnumLayer.BATCH_NORMALIZATION.value:
                self.model.add(BatchNormalization())
            elif lay["NAME"] == mb.EnumLayer.CONV2D.value:
                self.model.add(Conv2D(int(lay["count"]),
                                      kernel_size=int(lay["kernel_size"]),
                                      activation=str(lay["activation"]),
                                      padding=str(lay["padding"])
                                      )
                               )
        # este treba optimizer

        # optim_obj = p_json["optimizer"]
        # self.model.compile(loss=str(optim_obj["loss"]),
        #				   optimizer=str(optim_obj["optimizer"]),
        #				   metrics=[str(optim_obj["metrics"])])
        self.model.compile(loss="binary_crossentropy",
                           optimizer=self.optimizer,
                           metrics=['accuracy'])
        # ulozit to do DB
        self.save_state()

    def change_ref_data(self, new_ref_data):
        self.ref_data = new_ref_data
        self.is_changed = True

    def load_train_session_file(self):
        '''

        :return:  TRUE    - model sa prave trenuje
                  Subor   - model uz bol trenovany
                  None    - model este nebol trenovany nikdy
        '''
        print('loading file')
        self.locked_by_training = False
        if self.locked_by_training:
            # neda sa vratit jeho train session, ked sa trenuje
            return True
        else:
            if self.trained_on_dataset is None:
                # model este nebol trenovany vobec
                return None
            else:
                # model uz bol trenovany
                return "trainSession: [10,10,10,15,15,15], epoch: 5, loss:1000 ..."
        # TODO: najdenie suboru s historiu trainu

    def is_locked_by_training(self):
        return self.locked_by_training

    def is_trained_on_dataset(self):
        if self.trained_on_dataset is None:
            return False
        else:
            return True