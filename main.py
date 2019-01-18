import model
import keras
import sys
import data
import numpy as np
import GUI.plot_modified as plt

# entry point
if __name__ == "__main__":
    # kontrola dependences
    print("Interpreter version: " + sys.version)
    print("Keras version: " + keras.__version__)

    # start aplikacie
    print("Aplication started: OK (main)")

    # init glob. vars
    model = model.Model()
    data = data.Data()
    data.load_all_data()

    model.create_model()

    print(model.model_summary())
    model.train(data.train_data,data.train_labels)

    result = model.predict_image(np.expand_dims(data.train_data[0],axis=0))


    print(result)
    d = np.expand_dims(data.train_data[0],axis=0)
    ss = np.expand_dims(data.train_data[0:3], axis=0)

    predicted = model.model_generated_predictions(np.array(data.train_data),data.train_labels)
    plot = plt.Plot_modified()
    plot.plot_data(data.train_data,data.train_labels,predicted)
