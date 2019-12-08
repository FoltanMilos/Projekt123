from src.models.mlp.neuron import Neuron


class Layer:
    def __init__(self, layer_size=1, prev_layer_size=1, activation_function="sigmoid", weights=None, json=None):
        if json is None:
            self.outputs = [0] * layer_size
            self.prev_layer_size = prev_layer_size
            self.activation_function = activation_function
            if weights is not None:
                self.neurons = [Neuron(prev_layer_size, weights[i]) for i in range(layer_size)]
            else:
                self.neurons = [Neuron(prev_layer_size) for i in range(layer_size)]
        else:
            self.from_json(json)

    def evaluate(self, inputs):
        if self.prev_layer_size == 0:
            self.outputs = [self.neurons[i].activate(inputs[i], self.activation_function) for i in range(len(inputs))]
        else:
            self.outputs = [neuron.activate(inputs, self.activation_function) for neuron in self.neurons]
        return self.outputs

    def to_json(self):
        return {'prev_layer_size': self.prev_layer_size, 'activation_function': self.activation_function, 'size': len(self.outputs), 'neurons': [n.to_json() for n in self.neurons]}

    def from_json(self, json):
        self.prev_layer_size = json['prev_layer_size']
        self.activation_function = json['activation_function']
        self.outputs = [0] * json['size']
        self.neurons = [Neuron(json=n) for n in json['neurons']]
