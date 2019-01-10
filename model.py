from keras import layers, Sequential


### Trieda zodpovedna za model systemu
class Model:
    global model  #model programu

    def __init__(self):
        self.model = Sequential()
        self.model.add(layers.Dense(64, activation='relu'))