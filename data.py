import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image as img_proc

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

    def __init__(self,ref_model):
        self.ref_model= ref_model
        self.paths = {"T":None,
                      "R":None,
                      "V":None}
        self.is_new = None
        self.train_datagen = ImageDataGenerator(rescale=1. / 255,
                                                shear_range=0.2,
                                                zoom_range=0.2,
                                                horizontal_flip=True)
        #self.load_train_set()
        #self.load_test_set()
        #self.load_validation_set()

    # LOADING AS FILE ITERATOR
    def load_train_set(self):
        self.train_set = self.train_datagen.flow_from_directory(
            self.paths["R"],
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\train\\',
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            #save_to_dir='C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\ssss',
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.train_set

    def load_test_set(self):
        self.test_set = self.train_datagen.flow_from_directory(
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\',
            self.paths["T"],
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.test_set

    def load_validation_set(self):
        self.valid_set = self.train_datagen.flow_from_directory(
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\validation\\',
            self.paths["V"],
            target_size=(64, 64),
            batch_size=16,
            shuffle=False,
            classes=["malignant", "bening"],
            class_mode='binary')
        return self.valid_set

    def load_image_exante_flow(self, dir_full_path):
        """ Dovoluje nacitat viacero fotiek zo suboru"""
        images_exante_set = self.train_datagen.flow_from_directory(
            dir_full_path,
            target_size=(64, 64),
            batch_size=1,
            classes=["malignant", "bening"],
            shuffle=False,  # pre zachovanie poradia
            class_mode='binary')
        return images_exante_set

    def load_image_exante(self,file_full_path):
        """ Nacita jednu fotku zo suboru"""
        image_exante = img_proc.load_img(
            file_full_path,
            #'C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\prediction\\malignant\\ISIC_0028679.jpg',
            target_size=(64, 64))
        image_exante = img_proc.img_to_array(image_exante)
        image_exante = np.expand_dims(image_exante, axis=0)
        return image_exante

    def preproces_image(self,image):
        image = img_proc.img_to_array(image)
        image = image.reshape(shape=(64,64)) #OTESTOVAT
        image = np.expand_dims(image, axis=0)
        return image

    def load_state(self):
        ret_data_set = self.ref_model.ref_user.ref_db.select_statement(
            "select D_ID, M_ID, D_NAME, D_PATH, D_PATH_TYPE from PROJECTUSER.proj_data where m_id=" + str(self.ref_model.m_id) + "")
        if (len(ret_data_set) < 2):
            print("MODEL HAS NO DATA!!!!!!!!!!!!!!!!!!!!!!!!!")
        for row in ret_data_set:
            self.paths[row[4]] = row[3]
            self.name = row[2]
        self.is_new = True

    def save_state(self):
        print("[SAVE]: data")
        oo = 0
        if(self.is_new):
            for path_dict in self.paths:
                self.ref_model.ref_user.ref_db.insert_statement("insert into PROJECTUSER.proj_data( M_ID, D_NAME, D_PATH, D_PATH_TYPE) "
                    "values(:2, :3, :4, :5)",(self.ref_model.m_id,self.name,self.paths[path_dict],path_dict))
            #self.ref_model.ref_user.ref_db.commit()
        elif(self.is_changed):
            pass
            # update
        else:
            pass
            # uz tam su