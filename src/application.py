import sys
import keras
import user
import database_manipulation as dm
import string
import random


class Application:
    global active_model         # instancia triedy modelu, s ktorym sa pracuje

    global data                 # instancia triedy data

    global list_active_user     # list vsetkych userov v aplikacii

    global ref_db               # referencia na databazu

    global active_user          # instancia pre ulahceie pristupu k ulozene userovi
                                # ak jeho token nesedi, treba update cez najdenie usera

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")
        # pripojenie na DB
        self.ref_db = dm.DB_manip()

        self.list_active_user = []
        self.active_model = None

        sr = user.User(self, 3, self.ref_db, self.generate_unique_string())
        self.active_user = sr
       # model = mc.Model_cnn("Newestone model",sr,self)
        #model.create()
        #dat = dt.Data(model)
        #dat.paths = {"T": 'dataset/small_dataset/test',
        #              "R": 'dataset/small_dataset/train',
        #              "V": 'dataset/small_dataset/validation'}

        # tadeto sa budu menit datasety
        #model.change_ref_data(dat)
       # model.train()
        #model.create_model_from_json("")
        #model.summary()



        #sr.load_user_data()
        #self.list_active_user.append(sr)
        #self.active_user = sr


        #TESTOVANIE
     #3   modelForTest = sr.models.pop(0)
    #  modelForTest


        # self.db_connect.insert_returning_identity("")

        #self.active_user.save_user_data()

    """Najde usera, ktory je v zozname nacitanych userov ak je pouzivanie vsetkych userov potrebne
    :param id: id_usera
    """
    def find_user_by_id(self,id):
        if self.active_user.u_id == id:
            return self.active_user;
        for user in self.list_active_user:
            if(user.u_id==id):
                return user
        return None

    """Nahra vsetkych userov do pamate, len nenahra ich udaje. Ked sa prepnu useri, treba ich nechad cascadovo
    naloadovat
    """
    def load_actual_users(self):
        self.list_active_user = user.User.load_all_users_no_cascade(self, self.ref_db)


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
        res = self.ref_db.select_statement("select * from proj_user where u_name ='"+ credentials['username'] +"'")
        for row in res:
            if row[2] == credentials['pass']:
                identifier = self.generate_unique_string()
                logged_user = user.User(self, row[0], self.ref_db, identifier)
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
        # zrychleny check na active usera pre rychlost
        if self.active_user.indentifier == identification:
            return self.active_user
        else:
            for usr in self.list_active_user:
                if(usr.indentifier == identification):
                    return usr
        return False

    def get_models(self, user):
        jsonarray = []
        for model in user.models:
            jsonarray.append(model.model.to_json())
        return jsonarray

    """Vymeni aktivneho uzivatela s ulozenim povodneho ak je treba
    """
    def swap_active_user(self,user_id):
        self.active_user.save_user_data()
        usr = self.find_user_by_id(user_id)
        if(usr==None):
            self.active_user=self.active_user
        else:
            self.active_user


    def logout_user(self,user):
        try:
            self.list_active_user.remove(user)
        except Exception as e:
            return False


