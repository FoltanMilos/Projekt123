import model
import keras
import sys
import data

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

    model.create_model()


    #


