from src.models.mlp.layer import Layer
from numpy import dot, sqrt
import json


class Mlp:
    def __init__(self, layer_sizes=(1,1), activation_functions=("sigmoid", "sigmoid"), learning_rate=0.005, epsilon=0.1, weights=None, json=None):
        if json is None:
            self.train_hist = []
            self.epsilon = epsilon
            self.learning_rate = learning_rate
            self.layers = [Layer(layer_sizes[j], 0 if j == 0 else layer_sizes[j - 1], activation_functions[j]) for j in range(len(layer_sizes))]
            if weights is not None:
                self.set_weights(weights)
        else:
            self.from_json(json)

    def to_json(self):
        return {'learning_rate': self.learning_rate, 'epsilon': self.epsilon, 'layers': [l.to_json() for l in self.layers]}

    def from_json(self, d):
        self.epsilon = d['epsilon']
        self.learning_rate = d['learning_rate']
        for i in range(len(d['layers'])):
            d['layers'][i]['prev_layer_size'] = 0 if i == 0 else d['layers'][i-1]['NEURON_COUNT']
        self.layers = [Layer(json=l) for l in d['layers']]

    def train(self, inputs, labels, callback, epoch_count, image=False):
        for i in range(len(inputs)):
            if image:
                out = self.__predict_image__(inputs[i], labels[i])
            else:
                out = self.__predict__(inputs[i], labels[i])
            output_err = self.__calculate_output_error__(out, labels[i])
            weight_err = self.__backpropagate_error__(output_err)
            self.__adapt_synaptic_weights__(weight_err)

    def __calculate_output_error__(self, estimates, labels):
        return [self.layers[-1].neurons[i].__getattribute__("derivative_"+self.layers[-1].activation_function)()*sqrt((labels[i] - estimates[i])**2) for i in range(len(estimates))]

    def __backpropagate_error__(self, output_error):
        err = [[0 for neuron in layer.neurons] for layer in self.layers[:-1]]
        err.append(output_error)
        for m in range(len(self.layers[:-1])-1, 0, -1):
            for i in range(len(self.layers[m].neurons)):
                err[m][i] = self.layers[m].neurons[i].__getattribute__("derivative_"+self.layers[m].activation_function)()*dot([neuron.weights[i] for neuron in self.layers[m+1].neurons], err[m+1])
        return err

    def __predict__(self, inputs, target=[0]):
        for layer in self.layers:
            outputs = layer.evaluate(inputs)
            inputs = outputs
        return self.__step_array__(outputs, target)

    def __adapt_synaptic_weights__(self, error):
        for m in range(1, len(self.layers)):
            for i in range(len(self.layers[m].neurons)):
                for j in range(len(self.layers[m].neurons[i].weights)):
                    self.layers[m].neurons[i].weights[j] += self.learning_rate*error[m][i]*self.layers[m-1].outputs[j]

    def ex_post(self, inputs, labels, image=False):
        if image:
            return [self.__predict_image__(inputs[i], labels[i]) for i in range(len(inputs))]
        return [self.__predict__(inputs[i], labels[i]) for i in range(len(inputs))]

    def ex_ante(self, inputs, image=False):
        if image:
            return [self.__predict_image__(i) for i in inputs]
        return [self.__predict__(i) for i in inputs]

    def get_weights(self):
        return [[neuron.weights for neuron in layer.neurons] for layer in self.layers]

    def set_weights(self, weights):
        assert len(self.layers) == len(weights)
        for i in range(len(weights)):
            assert len(self.layers[i].neurons) == len(weights[i])
            for j in range(len(weights[i])):
                assert len(self.layers[i].neurons[j]) == len(weights[i][j])
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                self.layers[i].neurons[j] = weights[i][j]

    def __predict_image__(self, image, target=[0]):
        if len(image) == len(self.layers[0].neurons):
            return self.__predict__(image, target)
        raise Exception("Input length doesn't match input layer size")

    def __step_array__(self, n, target_list=[0]):
        return [self.__step__(n[i], target_list[i]) for i in range(len(target_list))]

    def __step__(self, n, target):
        if target == 0:
            if n < self.epsilon:
                return 0
            return 1
        else:
            if n > 1 - self.epsilon:
                return 1
            return 0

    def save(self, path_struct):
        with open(path_struct, 'w') as fp:
            json.dump(self.to_dict(), fp)
