import interface.model_interface as interface
from neural_nets.mlp.cv_wrapper import CrossValidation
from neural_nets.mlp.mlp import Mlp


class Model_mlp(interface.ModelInterface):
    def __init__(self):
        self.mlp = None

    def test_model(self, test_data, test_labels):
        return CrossValidation.cross_validate_mlp(1, test_data, test_labels, self.mlp)

    def create_model(self, layer_sizes, learning_rate=0.5, activation_function="sigmoid", epoch_count=10):
        self.mlp = Mlp(layer_sizes, learning_rate, activation_function, epoch_count)

    def predict_image(self, img):
        raise Exception("Unsupported function")

    def model_summary(self):
        raise Exception("Unsupported function")

    def train(self, train_data, train_labels):
        self.mlp.learn(train_data, train_labels)

    def load_model(self):
        self.mlp.load_model()

    def save_model(self):
        self.mlp.save_model()
