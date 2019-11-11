import interface.model_interface as interface
from models.mlp.cv_wrapper import CrossValidation
from models.mlp.mlp import Mlp

class Model_mlp(interface.ModelInterface):
    def load_state(self, state):
        pass

    def save_state(self):
        pass

    def __init__(self):
        self.mlp = None

    def test(self, test_data, test_labels):
        return CrossValidation.cross_validate_mlp(1, test_data, test_labels, self.mlp)

    def create(self, layer_sizes, learning_rate=0.5, activation_function="sigmoid", epoch_count=10):
        self.mlp = Mlp(layer_sizes, learning_rate, activation_function, epoch_count)

    def predict_image(self, img):
        raise Exception("Unsupported function")

    def summary(self):
        raise Exception("Unsupported function")

    def train(self, train_data, train_labels):
        self.mlp.learn(train_data, train_labels)

    def load(self):
        self.mlp.load()

    def save(self):
        self.mlp.save()
