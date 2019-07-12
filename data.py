from PIL import Image
import csv
import os
import numpy as np
import glob
import config as conf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image as img_proc

class Data:
    global train_set
    #global train_labels
    global valid_set
    #global valid_labels
    global test_set
    # global test_labels

    # file iterator
    global train_datagen

    def __init__(self):
        self.train_datagen = ImageDataGenerator(rescale=1. / 255,
                                                shear_range=0.2,
                                                zoom_range=0.2,
                                                horizontal_flip=True)
        self.load_train_set()
        self.load_test_set()
        self.load_validation_set()
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

    ## NEW PART - NEW LOADING AS FILE ITERATOR
    def load_train_set(self):
        self.train_set = self.train_datagen.flow_from_directory(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\train\\',
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            #save_to_dir='C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\ssss',
            classes=["malignant", "bening"],
            class_mode='binary')

        return self.train_set

    def load_test_set(self):
        self.test_set = self.train_datagen.flow_from_directory(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\',
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.test_set

    def load_validation_set(self):
        self.valid_set = self.train_datagen.flow_from_directory(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\validation\\',
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.valid_set

    def load_image_exante_flow(self):
        """ Dovoluje nacitat viacero fotiek zo suboru"""
        images_exante_set = self.train_datagen.flow_from_directory(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\',
            target_size=(64, 64),
            batch_size=1,
            classes=["malignant", "bening"],
            shuffle=False,  # pre zachovanie poradia
            class_mode='binary')
        return images_exante_set

    def load_image_exante(self):
        """ Nacita jednu fotku zo suboru"""
        image_exante = img_proc.load_img(
            'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\prediction\\malignant\\ISIC_0028679.jpg',
            target_size=(64, 64))
        image_exante = img_proc.img_to_array(image_exante)
        image_exante = np.expand_dims(image_exante, axis=0)
        return image_exante

    def preproces_image(self,image):
        image = img_proc.img_to_array(image)
        image = image.reshape(shape=(64,64)) #OTESTOVAT
        image = np.expand_dims(image, axis=0)
        return image

