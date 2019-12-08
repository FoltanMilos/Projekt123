from src.models.mlp.layer import Layer
from numpy import dot, sqrt


class Mlp:
    def __init__(self, layer_sizes=(1,1), learning_rate=0.005, epsilon=0.1, weights=None, json=None):
        if json is None:
            self.epsilon = epsilon
            self.learning_rate = learning_rate
            self.layers = [Layer(layer_sizes[j], 0 if j == 0 else layer_sizes[j - 1]) for j in range(len(layer_sizes))]
            if weights is not None:
                self.set_weights(weights)
        else:
            self.from_json(json)

    def from_json(self, json):
        self.epsilon = json['epsilon']
        self.learning_rate = json['learning_rate']
        self.layers = [Layer(json=l) for l in json['layers']]

    def to_json(self):
        return {'learning_rate': self.learning_rate, 'epsilon': self.epsilon, 'layers': [l.to_json() for l in self.layers]}

    def learn(self, inputs, labels):
        self.__backpropagation__(inputs, labels)

    def __backpropagation__(self, inputs, labels):
        for i in range(len(inputs)):
            out = self.__predict__(inputs[i])
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

    def __predict__(self, inputs):
        for layer in self.layers:
            outputs = layer.evaluate(inputs)
            inputs = outputs
        return [self.step(i) for i in outputs]

    def __adapt_synaptic_weights__(self, error):
        for m in range(1, len(self.layers)):
            for i in range(len(self.layers[m].neurons)):
                for j in range(len(self.layers[m].neurons[i].weights)):
                    self.layers[m].neurons[i].weights[j] += self.learning_rate*error[m][i]*self.layers[m-1].outputs[j]

    def test(self, inputs):
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

    def predict_image(self, image):
        if len(image) == len(self.layers[0].neurons):
            return self.__predict__(image)
        raise Exception("Input length doesn't match input layer size")

    def step(self, n):
        if n < self.epsilon:
            return 0
        elif n > 1 - self.epsilon:
            return 1
        return n

