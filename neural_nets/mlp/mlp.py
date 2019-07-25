from neural_nets.mlp.layer import Layer
from numpy import dot


class Mlp:

    def __init__(self, layer_sizes, learning_rate=0.5, activation_function="sigmoid", epoch_count=10):
        self.set_hyperparameters(learning_rate, activation_function, epoch_count)
        self.layers = [Layer(layer_sizes[j], 0 if j == 0 else layer_sizes[j-1]) for j in range(len(layer_sizes))]

    def learn(self, inputs, labels):
        for i in range(1, self.epoch_count+1):
            self.__backpropagation__(inputs, labels)

    def __backpropagation__(self, inputs, labels):
        for i in range(len(inputs)):
            out = self.__predict__(inputs[i])
            output_err = self.__calculate_output_error__(out, labels[i])
            weight_err = self.__backpropagate_error__(output_err)
            self.__adapt_synaptic_weights__(weight_err)

    def __calculate_output_error__(self, estimates, labels):
        return [self.layers[-1].neurons[i].__getattribute__("derivative_"+self.activation_function)()*(labels[i] - estimates[i]) for i in range(len(estimates))]

    def __backpropagate_error__(self, output_error):
        err = [[0 for neuron in layer.neurons] for layer in self.layers[:-1]]
        err.append(output_error)
        for m in range(len(self.layers[:-1])-1, 0, -1):
            for i in range(len(self.layers[m].neurons)):
                err[m][i] = self.layers[m].neurons[i].__getattribute__("derivative_"+self.activation_function)()*dot([neuron.weights[i] for neuron in self.layers[m+1].neurons], err[m+1])
        return err

    def __predict__(self, inputs):
        for layer in self.layers:
            outputs = layer.evaluate(inputs, self.activation_function)
            inputs = outputs
        return outputs

    def __adapt_synaptic_weights__(self, error):
        for m in range(1, len(self.layers)):
            for i in range(len(self.layers[m].neurons)):
                for j in range(len(self.layers[m].neurons[i].weights)):
                    self.layers[m].neurons[i].weights[j] += self.learning_rate*error[m][i]*self.layers[m-1].outputs[j]

    def test(self, inputs):
        return [self.__predict__(i) for i in inputs]

    def set_hyperparameters(self, learning_rate, activation_function, epoch_count):
        self.activation_function, self.learning_rate, self.epoch_count = activation_function, learning_rate, epoch_count

    def reset_weights(self):
        self.__init__([len(layer.neurons) for layer in self.layers], self.learning_rate, self.activation_function, self.epoch_count)

    def get_weights(self):
        raise Exception("Unsupported function")
