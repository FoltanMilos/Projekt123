import src.interface.model_interface as interface
from models.cnn.results_set import Results_set
import json
import config as conf
from models.mlp.mlp import Mlp
import data as dt


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
        self.callb = None
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
        pass

    def save_state(self):
        pass

    def load_train_session_file(self):
        pass

    def model_to_json(self):
        return {'model': self.model.to_json()}

    def train(self, dataset_name):
        pass

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
