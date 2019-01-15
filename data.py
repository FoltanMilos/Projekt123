from PIL import Image
import configuration as conf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

##ALL data informations and datasets with its labels
class Data:
    global train_data
    global train_labels

    global test_data
    global test_labels


    def __init__(self):
        ##NACITANIE DAT A ROZDELENIE DO DATASETOV podla conf
        try:
            img = mpimg.imread('ISIC_0000000.jpg')
            #self.show_image(img)
        except IOError:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py"+
                  " v premennej DIR!")

    #@param immage
    def show_image(self,img):
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show(block=True)
