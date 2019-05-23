import model
import keras
import sys
import data
import numpy as np
import matplotlib.pyplot as plt


class Backend:
    # instancia triedy model
    global model

    # instancia triedy data
    global data

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")

        # init data
        self.data = data.Data()
        self.data.load_all_data()
        self.data.load_all_labels()

        # init model
        self.model = model.Model()
        self.model.create_model()
        if(train == False):
            self.model.load_model()
            ## Pred predikciou musi byt spusteny test modelu (len pre nahranie vsetkych parametrov na miest)
            ## Staci aj s jednym obrazkom
            self.model.test_model(self.data.test_data[1:2],self.data.test_labels[1:2])
            print(self.model.model_summary())
        else:
            history_train = self.model.train(self.data.train_data,self.data.train_labels)
            self.model.test_model(self.data.test_data, self.data.test_labels)
            print(self.model.model_summary())
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


# entry point
if __name__ == "__main__":
    bck = Backend()