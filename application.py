import sys
import keras
import user
import database_manipulation as dm

class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global list_user            # list vsetkych userov v aplikacii

    global active_user          # aktivny pouzivatel, ktory je prihlaseny

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

        #testovanie
        self.active_user = self.list_user.pop(0)
        self.active_user.load_user_data()


        self.active_user.save_user_data()

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


    """Vymeni aktivneho uzivatela s ulozenim povodneho ak je treba
    """
    def swap_active_user(self,user_id):
        self.active_user.save_user_data()
        usr = self.find_user_by_id(user_id)
        if(usr==None):
            self.active_user=self.active_user
        else:
            self.active_user = usr

