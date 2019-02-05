from PIL import Image
import configuration as conf
import csv
import os
import numpy as np


##ALL data informations and datasets with its labels
class Data:
    global train_data
    global train_labels

    global test_data
    global test_labels

    def __init__(self):
        image_count =  os.listdir(os.path.dirname('data/images/')).__len__()
        self.train_data = []   #int(image_count/100)*conf.TRAIN_DATA
        self.train_labels = []  #int(image_count/100)*conf.TRAIN_DATA
        self.test_data = []     #int(image_count/100)*conf.TEST_DATA
        self.test_labels = []   #int(image_count/100)*conf.TEST_DATA

    ## NACITANIE DAT A ROZDELENIE DO DATASETOV podla conf
    def load_all_data(self):
        path_directory = os.listdir(os.path.dirname('data/images/'))
            # v csv je 0 ako benign -- nezhuby -- ten je OK
        index = 0
        try:
            for img_path in path_directory:
                if(index > 1000):
                    break
                    ##ten list dir neyvladne viac ....
                img = Image.open('data/images/' + img_path)
                # rozdelenie na train a test
                if index <= 950: #self.train_data.__len__()
                    self.train_data.append(np.array(img))
                    #self.train_labels.append(np.array([0]))
                else:
                    self.test_data.append(np.array(img))
                    #self.test_labels.append(np.array([0]))

                arr = self.train_data[0]
                # self.train_data.append(np.array(img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS))) - netreba lebo su rovnake
                print('Nacitany obrazok cislo  - {}   [ shape: {} ]'.format(index,arr.shape))
                index += 1
        except IOError as err:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py" +
                  " v premennej DIR!")
            print(str(err))

    def load_all_labels(self):
        with open('data/description/data_komplet.csv', 'r') as csvfile:
            subor = csv.reader(csvfile, delimiter=';')
            index = 0
            for i in subor:
                if(index > 0):
                    if (index > 1001):
                        break
                    if(index <= 951):
                        self.train_labels.append(np.array(i[1]))
                    else:
                        self.test_labels.append(np.array(i[1]))
                index+=1

    def load_solo_img(self,path):
        img = None
        try:
            img = Image.open(path)
        except:
            print("Nepodarilo sa nahrat fotku! ")
        return img