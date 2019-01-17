from PIL import Image
import configuration as conf
import matplotlib.pyplot as plt
import numpy as np

##ALL data informations and datasets with its labels
class Data:
    global train_data
    global train_labels

    global test_data
    global test_labels


    def __init__(self):
        ##NACITANIE DAT A ROZDELENIE DO DATASETOV podla conf
        try:
            self.train_data = []
            self.train_labels = []
            for i in range(0,4):
                img = Image.open('data/ISIC_000000' + str(i) +'.jpg')

                self.train_data.append(np.array(img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS)))
                #img = np.expand_dims(img, axis=0)
                arr = self.train_data[0]
                if i > 1 :
                    self.train_labels.append(np.array([0]))
                else:
                    self.train_labels.append(np.array([ 1]))

                print(arr.shape)

        except IOError:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py"+
                  " v premennej DIR!")

    #@param immage
    def show_image(self,img):
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show(block=True)
