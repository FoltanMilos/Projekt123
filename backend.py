import model
import keras
import sys
import data
import numpy as np
import GUI.plot_modified as plt


class Backend:
    # instancia triedy model
    global model

    # instancia triedy data
    global data

    def __init__(self):
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
        self.model.load_model()
        self.model.test_model(self.data.test_data,self.data.test_labels)  # musi byt pustena evualation
        print(self.model.model_summary())


        #result = model.predict_image(np.expand_dims(data.train_data[0],axis=0))


        #d = np.expand_dims(self.data.test_data[0:3],axis=0)
        #ss = np.expand_dims(self.data.test_data[0:3], axis=0)

        #predicted = self.model.model_generated_predictions(np.array(self.data.train_data),self.data.train_labels)
        #plot = plt.Plot_modified()
        #plot.plot_data(self.data.train_data,self.data.train_labels,predicted)


# entry point
if __name__ == "__main__":
    bck = Backend()