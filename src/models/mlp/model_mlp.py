import src.interface.model_interface as interface
from models.cnn.callbacks import LiveLearningCallback
from models.cnn.results_set import Results_set
import json
import config as conf
from models.mlp.mlp import Mlp
import data as dt
import os


class Model_mlp(interface.ModelInterface):

    def __init__(self, ref_user, ref_app, ref_data, model_name=None):
        self.json_structure = None
        self.ref_user = ref_user
        self.ref_app = ref_app
        self.ref_data = ref_data
        self.trained_on_dataset = None
        self.training_file = None
        self.locked_by_training = None
        self.static = None
        self.m_id = -1
        self.model = None
        self.callb = LiveLearningCallback(0)
        if model_name is None:
            self.is_new = False
            self.is_changed = False
        else:
            self.is_new = True
            self.is_changed = False
            self.name = model_name
            self.ref_res_proc = Results_set(self, True)
            # self.ref_res_proc.save_state()
            self.path_struct = None
            self.path_weights = None
            self.model = Mlp()

    def test(self, datasetName):
        pass

    def summary(self):
        pass

    def create_model_from_json(self, json):
        self.model.from_json(json)

    def predict_image(self, img):
        image = img.flatten()
        if len(image) == len(self.layers[0].neurons):
            return self.model.predict(image)
        raise Exception("Input length doesn't match input layer size")

    def load_state(self, state):
        self.m_id = int(state[0])
        self.path_struct = state[4]
        self.json_structure = None
        #self.path_weights = state[5]
        self.is_new = False
        self.is_changed = False
        self.name = state[5]
        if state[6] == 'F':
            self.locked_by_training = False
        else:
            self.locked_by_training = True
        self.trained_on_dataset = state[7]
        self.static = state[8]

        self.ref_data = dt.Data(self,self.trained_on_dataset)
        self.ref_data.load_state()

        self.ref_res_proc = Results_set(self, False)
        self.ref_res_proc.load_state()

        self.load()

    def save_state(self):
        if self.is_new:
            self.ref_res_proc.save_state()
            self.m_id = int(self.ref_app.ref_db.insert_returning_identity(
                "insert into "+ str(conf.database) +"_model(u_id,r_id,m_type,m_structure_path,model_name) values"
                "(" + str(self.ref_user.u_id) + ", " + str(
                    self.ref_res_proc.r_id) + ",'MLP','" + "','" + str(self.name) + "')"
                , "m_id"))
            os.mkdir(os.getcwd() + '/saved_model/mlp/' + str(int(self.m_id)))
            self.ref_app.ref_db.commit()

        if self.is_changed and self.is_new == False:
            self.ref_res_proc.save_state()
            dt = "'"+ str(self.trained_on_dataset) + "'"
            if self.trained_on_dataset is None:
                dt = "NULL"
            self.ref_app.ref_db.update_statement(
                "update "+ str(conf.database) +"_model set r_id=" + str(self.ref_res_proc.r_id) +
                ", m_structure_path='" + str(self.path_struct) + "', model_name='" + str(
                    self.name) + "',trained_on_dataset=" + str(dt)+ "  where m_id=" + str(self.m_id))
            self.ref_app.ref_db.commit()

    def load_train_session_file(self):
        if self.locked_by_training:
            return False
        else:
            if self.trained_on_dataset is None:
                return None
            else:
                try:
                    with open(self.ref_res_proc.train_result_path, 'r') as file_histo:
                        ret = json.load(file_histo)
                    return ret
                except:
                    self.ref_app.log.info("Model este nebol trenovany")
                return ret

    def model_to_json(self):
        return {'model': self.model.to_json()}

    def train(self, dataset_name):
        if self.trained_on_dataset is None:
            # este nebol trenovany, treba vybrat dataset
            self.ref_data = dt.Data(self,dataset_name)
            self.ref_data.load_state()
        self.ref_data.load_train_set()
        self.ref_data.load_validation_set()
        self.lock_training()
        self.callb.max_epoch = 10
        train_hist
        # nastavenie parametrov
        self.trained_on_dataset = self.ref_data.name
        self.is_changed = True
        self.is_new = False
        # res prov
        self.ref_res_proc.train_accuracy =  float(train_hist.history['accuracy'][len(train_hist.history['accuracy']) - 1])
        self.ref_res_proc.is_changed = True
        self.ref_res_proc.is_new = False
        self.ref_res_proc.train_result_path = "saved_model/mlp/" + str(int(self.m_id)) + "/train_history.json"
        self.save_state()
        self.save()
        self.save_train_history(train_hist)
        self.unlock_training()
        return train_hist

    def is_locked_by_training(self):
        return self.locked_by_training

    def is_trained_on_dataset(self):
        if self.trained_on_dataset is None:
            return False
        else:
            return True

    def load_test_session_file(self):
        ret = None
        if self.ref_res_proc.test_result_path is not None:
            with open(self.ref_res_proc.test_result_path, 'r') as file_histo:
                ret = json.load(file_histo)
        return ret

    def lock_training(self):
        self.locked_by_training = True
        self.ref_app.ref_db.update_statement("update "+str(conf.database)+"_model set locked_by_train='T' where m_id="+str(self.m_id))
        self.ref_app.ref_db.commit()

    def unlock_training(self):
        self.locked_by_training = False
        self.ref_app.ref_db.update_statement("update "+str(conf.database)+"_model set locked_by_train='F' where m_id="+str(self.m_id))
        self.ref_app.ref_db.commit()

    def save_train_history(self, train_history):
        pth = None
        if self.ref_res_proc.train_result_path is None:
            pth = "saved_model/mlp/" + str(int(self.m_id)) + "/train_history.json"
        else:
            pth = self.ref_res_proc.train_result_path
        with open(pth, 'w') as file_histo:
            for i in range(len(train_history.history['accuracy'])):
                train_history.history['accuracy'][i] = float(train_history.history['accuracy'][i])
                train_history.history['val_accuracy'][i] = float(train_history.history['val_accuracy'][i])
            json.dump(train_history.history, file_histo)
        self.ref_app.log.info("Training history has been saved.")

    def load(self):
        self.model = self.load_model(self.path_struct)
        self.ref_app.log.info("Loaded model from disk")

    def save(self):
        self.model.save(self.path_struct)
        self.ref_app.log.info("Saved model to disk")

    def load_model(self, path_struct):
        model = Mlp()
        with open(path_struct, 'r') as fp:
            d = json.load(fp)
        model.from_dict(d)
        return model
