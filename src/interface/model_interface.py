from abc import ABC, abstractmethod


class ModelInterface(ABC):
    global training_file
    global locked_by_training
    global trained_on_dataset
    global static
    
    @abstractmethod
    def train(self, datasetName):
        raise NotImplementedError

    @abstractmethod
    def test(self,datasetName):
        raise NotImplementedError

    @abstractmethod
    def summary(self):
        raise NotImplementedError

    @abstractmethod
    def create_model_from_json(self):
        raise NotImplementedError

    @abstractmethod
    def predict_image(self, img):
        raise NotImplementedError

    @abstractmethod
    def load_state(self,state):
        raise NotImplementedError

    @abstractmethod
    def save_state(self):
        raise NotImplementedError

    @abstractmethod
    def load_train_session_file(self):
        raise NotImplementedError

    @abstractmethod
    def load_test_session_file(self):
        raise NotImplementedError

    @abstractmethod
    def model_to_json(self):
        raise NotImplementedError
