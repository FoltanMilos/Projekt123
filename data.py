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
            for i in range(0,3):
                img = Image.open('data/ISIC_000000' + str(i) +'.jpg')
                self.train_data.append(np.array(img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS)))
            self.train_labels=self.train_data[0]
            #self.show_image(img)
        except IOError:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py"+
                  " v premennej DIR!")

    #@param immage
    def show_image(self,img):
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show(block=True)
