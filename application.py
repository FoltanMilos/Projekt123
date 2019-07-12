import sys
import keras
import matplotlib.pyplot as plt
import data as dt
import neural_nets.cnn.model_cnn as md_cnn
import nn_type
import database_manipulation as dm

class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global models               # zoznam vsetkych modelov, ktore su implementovane v aplikacii

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")

        # pripojenie na DB
        self.db_connect = dm.DB_manip()

        # initialization
        self.models = []

        # init data
        self.data = dt.Data()

        # init model
        self.active_model = md_cnn.Model_cnn(self.data)
        self.active_model.create_model()

        if(train == False):
            self.active_model.load_model()
            print(self.active_model.model_summary())

        else:
            history_train = self.active_model.train(self.data.train_set, self.data.valid_set)
            print(history_train)
            #self.active_model.test_model(self.data.test_data, self.data.test_labels)
            print(self.active_model.model_summary())

        #TEST MILOS
        self.active_model.predict_image_flow()

    # registruje model do zoznamu modelov
    def register_model(self,model):
        self.models.append(model)



    def predict(self):
        pass
        # z aktivneho modelu
        #img = self.data.train_data[1]
        #return self.active_model.predict_image(img)
        #return self.active_model.model_generated_predictions(self.data.test_data,self.data.test_labels)