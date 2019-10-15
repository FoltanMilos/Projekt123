from abc import ABC, abstractmethod

### --------------- I N T E R F A C E   M O D E L S --------------###
##              pevne definovanie rozhrania pre webove service      #
### --------------------------------------------------------------###
class ModelInterface(ABC):
    
    @abstractmethod
    def train(self, train_data, train_labels):
        raise NotImplementedError

    @abstractmethod
    def test_model(self):
        raise NotImplementedError

    @abstractmethod
    def model_summary(self):
        raise NotImplementedError

    @abstractmethod
    def create_model(self):
        raise NotImplementedError

    @abstractmethod
    def load_model(self):
        raise NotImplementedError

    @abstractmethod
    def save_model(self):
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