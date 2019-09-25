from enum import Enum

class EnumLayer(Enum):
    INPUT = "Input Layer"
    CONV2D = "Conv2D"
    FLATTENING = "Flattening"
    POOLING = "Max Pooling 2D"
    DENSE = "Dense"
    BATCH_NORMALIZATION = "batch normalization"

    def getValues(self):
        return list(EnumLayer)

class EnumActivations(Enum):
    SIGMOID = "sigmoid"
    RELU = "relu"
    LINEAR = "linear"

    def getValues(self,enum_layer):
        if(isinstance(enum_layer,EnumLayer)==False):
            raise Exception("Musi byt pouzita trieda enumu vrstvy")
        else:
            # vratenie atributov na nastavenie
            return list(EnumActivations)

class EnumLayerParameters(Enum):
    KERNEL_SIZE = "kernel_size"
    PADDING  = "padding"
    INPUT_SHAPE = "input shape"
    POOL_SIZE = "pool size"
    LOSS = "loss"
    OPTIMIZER = "optimizes"
    METRICS = "accuracy"
    NEURON_COUNT = "neuron count"

    def getValues(enum_layer):
        if (isinstance(enum_layer, EnumLayer) == False):
            raise Exception("Musi byt pouzita trieda enumu vrstvy")
        else:
            # vratenie atributov na nastavenie pre danu vrstvu
            r = []
            if(enum_layer is EnumLayer.DENSE):
                r.append(EnumLayerParameters.NEURON_COUNT)
                return r
            elif(enum_layer is EnumLayer.CONV2D):

                r.append(EnumLayerParameters.KERNEL_SIZE)
                r.append(EnumLayerParameters.INPUT_SHAPE)
                r.append(EnumLayerParameters.PADDING)
                return  r
            elif (enum_layer is EnumLayer.CONV2D):
                r.append(EnumLayerParameters.POOL_SIZE)
                return r
            elif (enum_layer is EnumLayer.FLATTENING):
                return r





