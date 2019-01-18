from PIL import Image
import configuration as conf
import csv
import os

##ALL data informations and datasets with its labels
class Data:
    global train_data
    global train_labels

    global test_data
    global test_labels

    def __init__(self):
        image_count =  os.listdir(os.path.dirname('data/images/')).__len__()
        self.train_data = [int(image_count/100)*conf.TRAIN_DATA]
        self.train_labels = [int(image_count/100)*conf.TRAIN_DATA]
        self.test_data = [int(image_count/100)*conf.TEST_DATA]
        self.test_labels = [int(image_count/100)*conf.TEST_DATA]

    ## NACITANIE DAT A ROZDELENIE DO DATASETOV podla conf
    def load_all_data(self):
        path_directory = os.listdir(os.path.dirname('data/images/'))
        with open('data/description/data_komplet.csv', 'rb') as csvfile:
            subor = csv.reader(csvfile, delimiter=',')
            # v csv je 0 ako benign -- nezhuby -- ten je OK
        index = 0

        try:
            for img_path in path_directory:
                img = Image.open('data/images/' + img_path)
                # rozdelenie na train a test
                if index <= self.train_data.__len__():
                    self.train_data.append(img)
                    self.train_labels.append(0)
                else:
                    self.test_data.append(img)
                    self.test_labels.append(0)
                    # self.train_data.append(np.array(img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS))) - netreba lebo su rovnake
                print('Nacitany obrazok cislo  - {}'.format(index))
                index += 1
        except IOError as err:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py" +
                  " v premennej DIR!")
            print(str(err))


