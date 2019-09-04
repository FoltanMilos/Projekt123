import sys
import keras
import user
import data as dt
import neural_nets.cnn.model_cnn as md_cnn
import nn_type
import database_manipulation as dm

class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global user

    global list_user            # list vsetkych userov v aplikacii

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")
        # pripojenie na DB
        self.db_connect = dm.DB_manip()

        # nacitanie userov applikacii
        # nacitava sa len jeden aktivny, nie je potrebne drzat vsetkych
        self.list_user = []
        self.load_actual_users()

        #nacitanie jedneho useera
        #self.user = user.User(self,3,self.db_connect)
        #self.list_user.append(self.user)
        #self.user.load_user_data()


    """Najde usera, ktory je v zozname nacitanych userov ak je pouzivanie vsetkych userov potrebne
    
    :param id: id_usera
    """
    def find_user_by_id(self,id):
        for user in self.list_user:
            if(user.u_id==id):
                return user
        return None

    """Nahra vsetkych userov do pamate, len nenahra ich udaje. Ked sa prepnu useri, treba ich nechad cascadovo
    naloadovat
    """
    def load_actual_users(self):
        self.list_user = user.User.load_all_users_no_cascade(self,self.db_connect)

