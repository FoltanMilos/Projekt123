import sys
import keras
import matplotlib.pyplot as plt
import data as dt
import neural_nets.cnn.model_cnn as md_cnn
import nn_type

class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global models               # zoznam vsetkych modelov, ktore su implementovane v aplikacii

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")

        # initialization
        self.models = []





        # init data
        self.data = dt.Data()
        self.data.load_all_data()
        self.data.load_all_labels()

        # init model
        self.active_model = md_cnn.Model_cnn()
        self.active_model.create_model()




        if(train == False):
            self.active_model.load_model()
            ## Pred predikciou musi byt spusteny test modelu (len pre nahranie vsetkych parametrov na miest)
            ## Staci aj s jednym obrazkom
            self.active_model.test_model(self.data.test_data[1:2], self.data.test_labels[1:2])
            print(self.active_model.model_summary())
        else:
            history_train = self.active_model.train(self.data.train_data, self.data.train_labels)
            self.active_model.test_model(self.data.test_data, self.data.test_labels)
            print(self.active_model.model_summary())
            ## vyvoj ucenia
            plt.figure(figsize=[8, 6])
            plt.plot(history_train.history['loss'], 'r', linewidth=3.0)
            plt.legend(['Training loss'], fontsize=18)
            plt.xlabel('Epochs ', fontsize=16)
            plt.ylabel('Loss', fontsize=16)
            plt.title('Loss Curves', fontsize=16)
            plt.show(block=True)

        #result = model.predict_image(np.expand_dims(data.train_data[0],axis=0))


        #d = np.expand_dims(self.data.test_data[0:3],axis=0)
        #ss = np.expand_dims(self.data.test_data[0:3], axis=0)

        #predicted = self.model.model_generated_predictions(np.array(self.data.train_data),self.data.train_labels)
        #plot = plt.Plot_modified()
        #plot.plot_data(self.data.train_data,self.data.train_labels,predicted)


    # registruje model do zoznamu modelov
    def register_model(self,model):
        self.models.append(model)
