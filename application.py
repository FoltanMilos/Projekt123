import sys
import keras
import user
import database_manipulation as dm
import pdb
import string
import random

class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global list_active_user     # list vsetkych userov v aplikacii



    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")
        # pripojenie na DB
        self.db_connect = dm.DB_manip()
        # nacitanie userov applikacii
        # nacitava sa len jeden aktivny, nie je potrebne drzat vsetkych
        self.list_active_user = []
        #self.load_actual_users()  # len na testovanie
        #testovanie
        # sr = user.User(self,3,self.db_connect,self.generate_unique_string())
        # sr.load_user_data()
        # self.list_active_user.append(sr)
        #
        #TESTOVANIE
        # modelForTest = sr.models.pop(0)
        # modelForTest


    """Najde usera, ktory je v zozname nacitanych userov ak je pouzivanie vsetkych userov potrebne
    
    :param id: id_usera
    """
    def find_user_by_id(self,id):
        for user in self.list_active_user:
            if(user.u_id==id):
                return user
        return None

    """Nahra vsetkych userov do pamate, len nenahra ich udaje. Ked sa prepnu useri, treba ich nechad cascadovo
    naloadovat
    """
    def load_actual_users(self):
        self.list_active_user = user.User.load_all_users_no_cascade(self,self.db_connect)


    """Vymeni aktivneho uzivatela s ulozenim povodneho ak je treba
    """
    def swap_active_user(self,user_id):
        self.active_user.save_user_data()
        usr = self.find_user_by_id(user_id)
        if(usr==None):
            self.active_user=self.active_user
        else:
            self.active_user = usr

    def validate_user(self, credentials):
        res = self.db_connect.select_statement("select * from proj_user where u_name ='"+ credentials['username'] +"'")
        for row in res:
            if row[2] == credentials['pass']:
                identifier = self.generate_unique_string()
                logged_user = user.User(self,row[0],self.db_connect, identifier)
                logged_user.load_user_data()
                self.list_active_user.append(logged_user)
                return {'identity':identifier, 'name': row[1]}
            else:
                return False

    def in_use(self,string):
        result = False
        for usr in self.list_active_user:
            if string == usr.ref_app:
                result = True
                break
        return result

    def generate_unique_string(self):
        alphabet = string.ascii_letters
        result = ''.join(random.choice(alphabet) for i in range(32))
        while(self.in_use(result)):
            result= ''.join(random.choice(alphabet) for i in range(32))
        return result

    def find_user_by_identification(self, identification):
        for usr in self.list_active_user:
            if(usr.indentifier == identification):
                return usr
        return False

    def get_models(self, user):
        jsonarray = []
        for model in user.models:
            jsonarray.append(model.model.to_json())
        return jsonarray

    def logout_user(self,user):
        try:
            self.list_active_user.remove(user)
        except Exception as e:
            return False