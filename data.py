from PIL import Image
import csv
import os
import numpy as np
import glob
import config as conf


##ALL data informations and datasets with its labels
class Data:
    global train_data
    global train_labels

    global test_data
    global test_labels

    global imagTrain
    global imagTest

    def __init__(self):
        self.train_data = []
        self.train_labels = []
        self.test_data = []
        self.test_labels = []
        self.imagTrain = []
        self.imagTest = []

    ## NACITANIE DAT A ROZDELENIE DO DATASETOV podla conf
    # ak je treba nahrat aj trenovacie data TRUE len ked sa pusta aj trenovanie
    # ked sa pusta testovanie bude sa to nahravat postupne
    def load_all_data(self): # is_need_to_load_train_data
        index = 0
        try:
            os.chdir('dataset/cnn/images/')
            for img_path in glob.iglob("*.jpg"):
                if(index > 15): #155
                    break
                img = Image.open(img_path)

                # rozdelenie na train a test
                if index <= 10: #self.train_data.__len__() #150
                    self.imagTrain.append(img)
                    self.train_data.append(np.array(img.resize((conf.IMG_SIZE_Y,conf.IMG_SIZE_X),Image.ANTIALIAS)))
                else:
                    self.imagTest.append(img)
                    self.test_data.append(np.array(img.resize((conf.IMG_SIZE_Y,conf.IMG_SIZE_X),Image.ANTIALIAS)))

                arr = self.train_data[0]
                # self.train_data.append(np.array(img.resize((conf.IMG_SIZE_X,conf.IMG_SIZE_Y),Image.ANTIALIAS))) - netreba lebo su rovnake
                print('Nacitany obrazok cislo  - {}   [ shape: {} ]'.format(index,arr.shape))
                index += 1
            ## spatne nastavenie pracovneho priecinka
            os.chdir('C:/SKOLA/7.Semester/Projekt 1/SarinaKristaTi/Projekt123')
        except IOError as err:
            print("Chyba pri otvarani suboru! Skontrolujte cestu v configuration.py" +
                  " v premennej DIR!")
            print(str(err))

    def load_all_labels(self):
        with open('dataset/cnn/description/data_komplet.csv', 'r') as csvfile:
            subor = csv.reader(csvfile, delimiter=';')
            index = 0
            for i in subor:
                if(index > 0):
                    if (index > 16):
                        break
                    if(index <= 11):
                        self.train_labels.append([i[1],i[0]])
                    else:
                        self.test_labels.append([i[1],i[0]])
                index+=1
    def load_solo_img(self,path):
        img = None
        try:
            img = Image.open(path)
        except:
            print("Nepodarilo sa nahrat fotku! ")
        return img