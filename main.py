import model
import keras
import sys

#entry point
if __name__ == "__main__":
    # kontrola dependences
    print("Interpreter version: " + sys.version)
    print("Keras version: " + keras.__version__)

    #start aplikacie
    print("Aplication started: OK (main)")

    #init glob. vars
    model = model.Model()
