from abc import ABC, abstractmethod

### --------------- I N T E R F A C E   M O D E L S --------------###
##              pevne definovanie rozhrania pre webove service      #
### --------------------------------------------------------------###
class ModelInterface(ABC):
    global training_file
    global locked_by_training
    global trained_on_dataset
    global static
    
    @abstractmethod
    def train(self):
        raise NotImplementedError

    @abstractmethod
    def test(self):
        raise NotImplementedError

    @abstractmethod
    def summary(self):
        raise NotImplementedError

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def save(self):
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