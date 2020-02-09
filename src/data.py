import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image as img_proc
import config as conf

class Data:
    global train_set
    global valid_set
    global test_set

    global train_datagen            # file iterator

    global paths                    # cesty k suborom

    global ref_model                # ref k modelu
    global is_changed               # ak sa zmenia dake cesty treba update
    global is_new                   # treba ulozit
    global name                     # nazov datasetu
    global d_id                     # id data
    global path_to_desc             # cesta k svojim popisom
    global count                    # pocet fotiek v danom type setu T,R,V
    global data_description         # popis modelu
    global count_bening             # count_all - malig - unclassed
    global count_malig
    global count_unspecified
    global link_dataset
    global img_size
    global count_all_pics           # v celom datasete T + R + V

    def __init__(self,ref_model,dataset_name):
        self.ref_model= ref_model
        self.paths = {"T":None,
                      "R":None,
                      "V":None}
        self.is_new = None
        self.name = dataset_name
        self.train_datagen = ImageDataGenerator(rescale=1. / 255,
                                                shear_range=0.2,
                                                zoom_range=0.2,
                                                horizontal_flip=True)
        self.is_new=False
        self.is_changed=False
        self.count = -1
        self.data_description = ""
        self.path_to_desc = ""
        self.count_bening = {"T":None,
                      "R":None,
                      "V":None}
        self.count_malig = {"T":None,
                      "R":None,
                      "V":None}
        self.count_unspecified = {"T":None,
                      "R":None,
                      "V":None}
        self.link_dataset = ""
        self.img_size = ""
        self.count_all_pics = -1

    # LOADING AS FILE ITERATOR
    def load_train_set(self):
        self.train_set = self.train_datagen.flow_from_directory(
            #self.path + '\\dataset\\main_dataset\\train\\',
            self.paths["R"],
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\train\\',
            target_size=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y),
            batch_size=16,
            shuffle=False,
            #save_to_dir='C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\ssss',
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.train_set

    def load_test_set(self):
        self.test_set = self.train_datagen.flow_from_directory(
            self.paths["T"],
            target_size=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.test_set

    def load_validation_set(self):
        self.valid_set = self.train_datagen.flow_from_directory(
            #self.path + '\\dataset\\main_dataset\\validation\\',
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\validation\\',
            self.paths["V"],
            target_size=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.valid_set

    def load_image_exante_flow(self, dir_full_path):
        """ Dovoluje nacitat viacero fotiek zo suboru"""
        images_exante_set = self.train_datagen.flow_from_directory(
            dir_full_path,
            target_size=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y),
            batch_size=1,
            classes=["malignant", "bening"],
            shuffle=False,  # pre zachovanie poradia
            class_mode='binary')
        return images_exante_set

    def load_image_exante(self,file_full_path):
        """ Nacita jednu fotku zo suboru"""
        image_exante = img_proc.load_img(
            file_full_path,
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\main_dataset\\prediction\\malignant\\ISIC_0028679.jpg',
            target_size=(conf.IMG_SIZE_X, conf.IMG_SIZE_Y))
        image_exante = img_proc.img_to_array(image_exante)
        image_exante = np.expand_dims(image_exante, axis=0)
        return image_exante

    def preproces_image(self,image,tupple_size):
        image = img_proc.img_to_array(image)
        image.resize((tupple_size[0],tupple_size[1],3),refcheck=False)
        image = np.expand_dims(image, axis=0)
        return image

    def load_state(self):
        if self.name is not None:
            # KED MODEL ESTE NEMA PRIRADENE DATA LEBO NEBOL TRENOVANY
            ret_data_set = self.ref_model.ref_app.ref_db.select_statement(
                "select * from "+str(conf.database)+"_data where d_name='" + str(self.name.lower()) + "'")
            for row in ret_data_set:
                self.d_id = row[0]
                self.paths[row[3]] = row[2]
                self.name = row[1]
                self.count = row[5]
                self.data_description = row[6]
                self.path_to_desc = row[4]
                self.count_bening[row[3]] = row[7]
                self.count_malig[row[3]] = row[8]
                self.count_unspecified[row[3]] = row[9]
                self.link_dataset = row[10]
                self.img_size = row[11]
                self.count_all_pics = row[12]

    def save_state(self):
        returned_id_data = None
        if self.is_new:
            for path_dict in self.paths:
                returned_id_data = self.ref_model.ref_app.ref_db.insert_returning_identity("insert into "+ str(conf.database) +"_data( M_ID, D_NAME, D_PATH, D_PATH_TYPE) values "
                    "("+str(self.ref_model.m_id)+",'"+str(self.name)+"','"+str(self.paths[path_dict])+"','"+str(path_dict)+"')","d_id")
        elif(self.is_changed):
            pass
            for path_dict in self.paths:
                self.ref_model.ref_app.ref_db.update_statement("update "+ str(conf.database) +"_data "
                        "set m_id:=:1 d_name:=:2 d_path:=:3 d_path_type:=:4 where d_id="+self.d_id+"",
                        (self.ref_model.m_id,self.name,self.paths[path_dict],path_dict))
        else:
            pass
        return returned_id_data

    def find_photo_description(self, string):
        if self.path_to_desc is not None:
            with open(self.path_to_desc) as file:
                description = file.read()
                for st in string:
                    pass
                    # find in files description
        return description

    def to_json(self):
        headers = {}
        headers["DatasetUsed"] = str(self.name)
        headers["All photo count"] = str(self.count_all_pics)
        headers["TRAIN - bening"] = str(self.count_bening["R"])
        headers["TRAIN - malig"] = str(self.count_malig["R"])
        headers["TRAIN - unspecified"] = str(self.count_unspecified["R"])
        headers["TEST - bening"] = str(self.count_bening["T"])
        headers["TEST - malig"] = str(self.count_malig["T"])
        headers["TEST - unspecified"] = str(self.count_unspecified["T"])
        headers["VALID - bening"] = str(self.count_bening["V"])
        headers["VALID - malig"] = str(self.count_malig["V"])
        headers["VALID - unspecified"] = str(self.count_unspecified["V"])
        headers["Dataset source"] = self.link_dataset
        headers["IMG size"] = str(self.img_size)
        headers["DatasetDesc"] = str(self.data_description)
        return headers