import sys
import keras
import src.user as user
import src.db.database_manipulation as dm
import string
import random
import src.models.cnn.model_cnn as cnn_md
import src.models.mlp.model_mlp as mlp_md
import src.models.genetic_alg.model_gen_alg as gen_md
import src.enum.enum_model as enum_model


class Application:
    global list_static_models  # instancia listu s modelov, s ktorymi sa pracuje

    global active_static_model # staticky model aktivny

    global list_active_user     # list vsetkych userov v aplikacii

    global ref_db               # referencia na databazu

    def __init__(self,train):
        # kontrola dependences
        print("Interpreter version: " + sys.version)
        print("Keras version: " + keras.__version__)
        print("Aplication started: OK (main)")
        # pripojenie na DB
        self.ref_db = dm.DB_manip()
        # init aplikacie
        self.list_active_user = []
        self.list_static_models = []
        self.active_static_model = None

        # natiahnutie statickych modelov
        self.load_all_static_models()

        ## testovanie no FE
        # VYHODIT
        import src.models.cnn.model_cnn as mc
        #credentials = {}
        #credentials['username'] = 'admin'
        #credentials['pass'] = 'admin'
        #self.validate_user(credentials)
        #self.list_active_user[0].indentifier = 'MgtKbChIBsFpumdwizuSeDnxXjBpDowo'

        #model = mc.Model_cnn("EXAMPLE",self.list_active_user[0],self,None)
        #model.is_new = True
        #dc = {}
        #dc["modelName"] = "EXAMPLE"
        #model.create_model_from_json(dc)

        #model = self.list_static_models[0]
        #hist = model.train("small_dataset")
        #hist_test = model.test("data(10015)")

       # hist = model.train("small_dataset")
        #print(hist)

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
        for usr in self.list_active_user:
            if(usr.indentifier == identification):
                return usr
        return None

    def logout_user(self,user):
        try:
            self.list_active_user.remove(user)
        except Exception as e:
            return False


    def get_static_models(self):
        jsonarray = []
        for model in self.list_static_models:
            jsonarray.append(model.model_to_json())
        return jsonarray

    def swap_active_static_model(self,model_id):
        for md in self.list_static_models:
            if md.m_id == model_id:
                self.active_static_model = md
                return self.active_static_model
        return self.active_static_model


    def load_all_static_models(self):
        result_stat_models = self.ref_db.select_statement("select * from proj_model where m_static = 'S'")
        for res_static_md in result_stat_models:
            if res_static_md[4] == enum_model.Nn_type.CNN.value:
                new_static_cnn_model = cnn_md.Model_cnn("",None,self)
                new_static_cnn_model.load_state(res_static_md)
                self.list_static_models.append(new_static_cnn_model)
            elif res_static_md[4] == enum_model.Nn_type.MLP.value:
                #TODO dorobit
                new_static_mlp_model = None
                new_static_mlp_model.load_state(res_static_md)
                self.list_static_models.append(new_static_mlp_model)
            elif res_static_md[4] == enum_model.Nn_type.GEN.value:
                # TODO dorobit
                new_static_gen_model = None
                new_static_gen_model.load_state(res_static_md)
                self.list_static_models.append(new_static_gen_model)

    def check_user_name(self,username):
        result = self.ref_db.select_statement("select count(u_name) from proj_user where u_name="+username.lower())
        if int(result[0]) > 0:
            # nie je to ok, narusienie jedinecnosti
            return False
        else:
            return True

    def create_user(self, username, password):
        result = self.ref_db.insert_statement("insert into proj_user(u_name,u_password,u_active,u_note,u_privileges)"
                    " values(:1,:2,:3,:4,:5)",[username,password,'N','vytvoreny cez app','L'])
        self.ref_db.commit()
        return True