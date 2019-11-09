import pickle
import src.models.result as resClass
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import numpy as np
from keras.models import model_from_json
import src.config as conf
import src.interface.model_interface as interface
import tensorflow.keras.initializers
import src.models.cnn.results_set as ResultSet
import os
import json
import src.enum.enum_model_builder as mb
import src.data as dt
import src.models.cnn.callbacks as callbck
import random
import tensorflow as tf
from tensorflow.keras import  backend as K
from tensorflow.keras.models import load_model
import threading as th
import time


class Model_cnn(interface.ModelInterface):
    #global model  # instancia modelu keras
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
    global json_structure # struktura modelu z buildera

    def __init__(self, model_name, ref_user, ref_app, ref_data=None):
        # povinne parametre
        self.json_structure = None
        self.ref_user = ref_user
        self.ref_app = ref_app
        self.ref_data = ref_data
        self.trained_on_dataset = None
        self.training_file= None
        self.locked_by_training= None
        self.static = None
        self.m_id = -1
        self.model = None
        self.callb = callbck.LiveLearningCallback(0)

        if model_name == "":
            # prazdna instania, do ktorej sa naloaduju data
            self.is_new = False
            self.is_changed = False
        else:
            # instancia, ktora bola nanovo vytvorena. Pozor, vypyta si naspat ID z db, podla neho sa vytvaraju priecinky
            self.is_new = True
            self.is_changed = False
            self.name = model_name
            self.ref_res_proc = ResultSet.Results_set(self, True)
            # self.ref_res_proc.save_state()
            self.path_struct = None
            self.path_weights = None
            self.model = Sequential()
        self.optimizer = tensorflow.keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
            # ADADELTA --> an adaptive learning rate method
            #  Adadelta is a more robust extension of Adagrad that adapts learning rates based on a moving window of gradient updates,
            #  instead of accumulating all past gradients. This way, Adadelta continues learning even when many updates have been done.
            #  Compared to Adagrad, in the original version of Adadelta you don't have to set an initial learning rate. In this version,
            #  initial learning rate and decay factor can be set, as in most other Keras optimizers.
        self.initializer = tensorflow.keras.initializers.glorot_uniform(conf.initializer_seed)
        self.bias_initializer = tensorflow.keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
            #self.save_state()

    # Ulozenie historie trenovania
    def save_train_history(self, train_history):
        # najpr do result setu
        pth = None
        if self.ref_res_proc.train_result_path is None:
            pth = "saved_model/cnn/" + str(int(self.m_id)) + "/train_history.json"
        else:
            pth = self.ref_res_proc.train_result_path
        with open(pth, 'w') as file_histo:
            for i in range(len(train_history.history['accuracy'])):
                train_history.history['accuracy'][i] = float(train_history.history['accuracy'][i])
                train_history.history['val_accuracy'][i] = float(train_history.history['val_accuracy'][i])
            json.dump(train_history.history, file_histo)
        self.ref_app.log.debug("Training history has been saved.")

    # Trenovanie
    def train(self,dataset_name):
        if self.trained_on_dataset is None:
            # este nebol trenovany, treba vybrat dataset
            self.ref_data = dt.Data(self,dataset_name)
            self.ref_data.load_state()
        self.ref_data.load_train_set()
        self.ref_data.load_validation_set()
        self.callb.max_epoch = 10
        self.lock_training()
        train_hist = self.model.fit_generator(
            self.ref_data.train_set, steps_per_epoch=10, epochs=self.callb.max_epoch,
            validation_data=self.ref_data.valid_set,
            validation_steps=5,
            callbacks=[EarlyStopping(monitor='accuracy',
                                     patience=200,
                                     verbose=1),
                      # callbck.LiveLearningCallback()
                       self.callb
                       ])
        # nastavenie parametrov
        self.trained_on_dataset = self.ref_data.name
        self.is_changed = True
        self.is_new = False
        # res prov
        self.ref_res_proc.accuracy =  float(train_hist.history['accuracy'][len(train_hist.history['accuracy'])-1])
        self.ref_res_proc.is_changed = True
        self.ref_res_proc.is_new = False
        self.save_state()
        self.save()
        self.save_train_history(train_hist)
        self.unlock_training()
        return train_hist

    # zlozenie modelu
    def summary(self):
        return self.model.summary()

    # Vytvorenie modelu od podlahy
    def create(self):
        # VSTUPNA
        self.model.add(Conv2D(64,
                              kernel_size=3,
                              #activation='relu',
                              #padding='valid',
                              #bias_initializer=self.bias_initializer,
                              input_shape=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y, 3)
                              #kernel_initializer=self.initializer
                              )
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
                           optimizer="adam",
                           metrics=['accuracy'])
        return self.model

    def load(self):
        self.model = load_model(self.path_struct)
        self.ref_app.log.debug("Loaded model from disk")

    def save(self):
        self.model.save(self.path_struct,save_format='h5')
        self.ref_app.log.debug("Saved model to disk")

    # Model evaluation
    def test(self, dataset_name, is_fast_test=False):
        # nahratie datasetu
        if self.ref_data is None or ( dataset_name is not None and self.ref_data.name != dataset_name):
            self.ref_data = dt.Data(self, dataset_name)
            self.ref_data.load_state()
        # ak chcem pustit rychlu evaluation
        if is_fast_test:
            self.ref_app.log.debug('Model evaulation(Fast test):')
            result = self.model.evaluate_generator(self.ref_data.load_test_set(),verbose=1)
            self.ref_app.log.debug('Evaluation completed:')
            i = 0
            for score in result:
                self.ref_app.log.debug('Name:{} Value:{}'.format(self.model.metrics_names[i], score))
                i += 1
            self.ref_app.log.debug('=========================')
            return result[0], result[1]
        else:
            # co sa ulozi do suboru na precitanie
            data_to_return = self.ref_data.load_test_set()
            result = self.model.predict_generator(data_to_return,verbose = 1)
            # process data results
            self.ref_res_proc.process_result_matrix(result,data_to_return[0][1],threshold=0.75)
            # zapisanie historie testovania
            test_history = {}
            header = self.ref_res_proc.to_json()
            results_list = []
            i = 0
            for res in result:
                universal_dict = {}
                metada_dummy = resClass.Metadata("Male", "26", "Bening", "serial imaging showing no change", "True")
                tmp_res = resClass.Result(res[0], "Bening", metada_dummy, None)
                universal_dict["Result"] = tmp_res.to_json()
                universal_dict["PhotoPath"] = str(data_to_return.filepaths[i])
                results_list.append(universal_dict)
                i += 1
            test_history["tested_results"] = results_list
            test_history["model_header"] = header
            test_history["dataset_header"] = self.ref_data.to_json()
            with open("saved_model/cnn/" + str(int(self.m_id)) + "/test_history.json", "w+") as json_file:
                json.dump(test_history, json_file)

            self.ref_res_proc.test_result_path = "saved_model/cnn/" + str(int(self.m_id)) + "/test_history.json"
            self.ref_res_proc.is_changed = True
            self.ref_res_proc.is_new = False
            self.ref_res_proc.save_state()
            return test_history

    def predict_image(self, image=None):
        """Predikcia jedneho obrazku"""
        if (image is None):
            raise Exception("Error by predict image. Image is None!")
        image = self.ref_data.preproces_image(image)
        ppp = self.model.predict_classes(image)
        predicted = self.model.predict(image)
        # vytvorenie triedy vysledku clasifikacie
        metada_dummy = resClass.Metadata("Male","26","Bening","serial imaging showing no change","True")
        result_class = resClass.Result(predicted[0][0],ppp[0][0],metada_dummy,None)
        return result_class.to_json()

    # TODO: na predikciu dakeho vaciseho sbor
    def predict_image_flow(self):
        #self.load()
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
        self.path_struct = state[5]
        self.json_structure = None
        #self.path_weights = state[5]
        self.is_new = False
        self.is_changed = False
        self.name = state[6]
        if state[7] == 'F':
            self.locked_by_training = False
        else:
            self.locked_by_training = True
        self.trained_on_dataset = state[8]
        self.static = state[9]

        # dotiahnutie dat
        self.ref_data = dt.Data(self,self.trained_on_dataset)
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
            self.m_id = int(self.ref_app.ref_db.insert_returning_identity(
                "insert into proj_model(u_id,r_id,m_type,m_structure_path,model_name) values"
                "(" + str(self.ref_user.u_id) + ", " + str(
                    self.ref_res_proc.r_id) + ",'CNN','" + "','" + str(self.name) + "')"
                , "m_id"))
            # ak je novy model, treba  u vytvorit este aj folder
            os.mkdir(os.getcwd() + '/saved_model/cnn/' + str(int(self.m_id)))
            self.ref_app.ref_db.commit()

        if self.is_changed and self.is_new == False:
            # najprv result_set
            self.ref_res_proc.save_state()
            # model
            dt = "'"+ str(self.trained_on_dataset) + "'"
            if self.trained_on_dataset is None:
                dt = "NULL"
            self.ref_app.ref_db.update_statement(
                "update proj_model set r_id=" + str(self.ref_res_proc.r_id) +
                ", m_structure_path='" + str(self.path_struct) + "', model_name='" + str(
                    self.name) + "',trained_on_dataset=" + str(dt)+ "  where m_id=" + str(self.m_id))
            self.ref_app.ref_db.commit()

    def model_to_json(self):
        ret_json = {}
        headers = {}
        #hlavicka modelu
        headers["Name"] = self.name
        headers["Accuracy"] = self.ref_res_proc.accuracy
        headers["ModelId"] = self.m_id
        headers["ModelType"] = "CNN"

        # z datasetu
        dataset_json = None
        if self.trained_on_dataset is not None:
            dataset_json = self.ref_data.to_json()

        ret_json["model_header"] = headers
        ret_json["data_header"] = dataset_json

        # model a jeho vrstvy
        #with open("saved_model/cnn/" +str(self.m_id) +"/json.json", 'r') as file:
        #    ret_json["layers"] = json.loads(file.read())
        ret_json["layers"] = self.load_file_structure()

        return ret_json

    def load_file_structure(self):
        with open("saved_model/cnn/" + str(self.m_id) + "/json.json", 'r') as file:
            ret = json.loads(file.read())
        return ret

    def create_model_from_json(self, p_json):
        self.json_structure = p_json
        self.name = p_json["modelName"]
        self.model = Sequential()
        #with open('other_files/jsonCreate', 'r') as jsons:
         #   p_json = json.load(jsons)
        for lay in p_json["layers"]:
            if lay["class"] == mb.EnumLayer.INPUT.name.upper():
                self.model.add(Conv2D(int(lay["NEURON_COUNT"]),
                                      kernel_size=int(str(lay["KERNEL_SIZE"]).split('x')[0].split(',')[0]),
                                      activation=str(lay["ACTIVATION"]).lower(),
                                      padding=str(lay["PADDING"]).lower(),
                                      bias_initializer=self.bias_initializer,
                                      #input_shape=(64,64,3),
                                      #kernel_initializer=self.initializer
                                      input_shape=(int(str(lay["INPUT_SHAPE"]).split('x')[0].split(',')[0]),
                                                   int(str(lay["INPUT_SHAPE"]).split('x')[0].split(',')[1]),
                                                   3)
                                      )
                               )
            elif lay["class"] == mb.EnumLayer.FLATTENING.name.upper():
                self.model.add(Flatten())
            elif lay["class"] == mb.EnumLayer.POOLING.name.upper():
                self.model.add(MaxPooling2D(pool_size=(int(str(lay["POOL_SIZE"])),
                                                       int(str(lay["POOL_SIZE"]))))
                               )
            elif lay["class"] == mb.EnumLayer.DENSE.name.upper():
                self.model.add(Dense(int(str(lay["NEURON_COUNT"]))
                                     , activation=str(lay["ACTIVATION"]).lower()))
            elif lay["class"] == mb.EnumLayer.BATCH_NORMALIZATION.name.upper():
                self.model.add(BatchNormalization())
            elif lay["class"] == mb.EnumLayer.CONV2D.name.upper():
                self.model.add(Conv2D(int(lay["NEURON_COUNT"]),
                                      kernel_size=int(str(lay["KERNEL_SIZE"]).split('x')[0].split(',')[0]),
                                      activation=str(lay["ACTIVATION"]).lower(),
                                      padding=str(lay["PADDING"]).lower()
                                      )
                               )
        self.model.compile(loss=str(p_json["loss"]),
        				   optimizer=str(p_json["optimizer"]),
        				   metrics=[str(p_json["metrics"])])

        # ulozit to do DB
        self.save_state() # toto je kvoli vrateniu ID
        self.path_struct = 'saved_model/cnn/' + str(int(self.m_id)) + '/model'
        self.is_new = False
        self.is_changed = True
        self.save_state() # treba ulozit cesty k suborom
        #ulozenie struktury modelu
        self.save()

        # ulozenie json create model
        with open("saved_model/cnn/"+ str(int(self.m_id)) +"/json.json", "w+") as json_file:
            json.dump(self.json_structure,json_file)

        return self.m_id

    #def change_ref_data(self, dataset_id):
    ##    self.ref_data = dt.Data(self)
     #   self.ref_data.d_id = dataset_id
     #   self.ref_data.load_state()
     #   self.is_changed = True

    def load_train_session_file(self):
        '''

        :return:  TRUE    - model sa prave trenuje
                  Subor   - model uz bol trenovany
                  None    - model este nebol trenovany nikdy
        '''
        #ret_dic = {}
        #ret_dic["train_history"] =None
        #if self.json_structure is None:
            #ret_dic["model_info"] = self.load_file_structure()
        #else:
        #    ret_dic["model_info"] = self.model_to_json()
        #if self.ref_data.name is None:
        #    ret_dic["dataset_info"] = None
        #else:
        #    ret_dic["dataset_info"] = ref_data.to_json()
        if self.locked_by_training:
            # neda sa vratit jeho train session, ked sa trenuje
            return True
        else:
            if self.trained_on_dataset is None:
                # model este nebol trenovany vobec
                return None
            else:
                # model uz bol trenovany

                try:
                    with open(self.ref_res_proc.train_result_path, 'r') as file_histo:
                        ret = json.load(file_histo)
         #               ret_dic["train_history"] = json.load(file_histo)
                    return ret
                except:
                    self.ref_app.log.debug("Model este nebol trenovany")
                return ret

    def is_locked_by_training(self):
        return self.locked_by_training

    def is_trained_on_dataset(self):
        if self.trained_on_dataset is None:
            return False
        else:
            return True


    def load_test_session_file(self):
        ret = None
        if self.ref_res_proc.test_result_path is not None:
            with open(self.ref_res_proc.test_result_path, 'r') as file_histo:
                ret = json.load(file_histo)
        return ret

    def lock_training(self):
        self.locked_by_training = True
        self.ref_app.ref_db.update_statement("update proj_model set locked_by_train='T' where m_id="+str(self.m_id))
        self.ref_app.ref_db.commit()

    def unlock_training(self):
        self.locked_by_training = False
        self.ref_app.ref_db.update_statement("update proj_model set locked_by_train='F' where m_id="+str(self.m_id))
        self.ref_app.ref_db.commit()