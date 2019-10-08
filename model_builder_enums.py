from enum import Enum

class EnumLayer(Enum):
    INPUT = "Input Layer"
    CONV2D = "Conv2D"
    FLATTENING = "Flattening"
    POOLING = "Max Pooling 2D"
    DENSE = "Dense"
    BATCH_NORMALIZATION = "batch normalization"



    def getValues():
        map = {}
        classNames = []
        for data in EnumLayer:
            map[data.name] =  data.value
            classNames.append({'id' : data.name, 'name': data.value})
        return map,classNames

class EnumActivation(Enum):
    SIGMOID = "sigmoid"
    RELU = "relu"
    LINEAR = "linear"

    def getValues():
            # vratenie atributov na nastavenie
            result = []
            for data in EnumActivation:
                result.append({"id": data.name, "name": data.value})
            return result

class EnumLayerParameters(Enum):
    #attr = tuple(ID,display_name, ExpectedVale)
    KERNEL_SIZE = ("KERNEL_SIZE","kernel_size", ["number","number"])
    PADDING  = ("PADDING","padding", "number")
    INPUT_SHAPE= ("INPUT_SHAPE","input shape", ["number","number"])
    POOL_SIZE = ("POOL_SIZE","pool size","number")
    LOSS = ("LOSS","loss","{}")
    OPTIMIZER = ("OPTIMIZER","optimizer","{}")
    METRICS = ("METRICS","accuracy","{}")
    NEURON_COUNT = ("NEURON_COUNT","neuron count", "number")
    ACTIVATION = ("ACTIVATION", 'activation', '{}')
    @staticmethod
    def getValues(enum_layer):
        values = [item.value for item in EnumLayer]
        if (not enum_layer in values):
            raise Exception('must be member of EnumLayers')

        r = []
        if(enum_layer is EnumLayer.DENSE.value):
            r.append(EnumLayerParameters.NEURON_COUNT.value)
            return r
        elif(enum_layer is EnumLayer.CONV2D.value):

            r.append(EnumLayerParameters.KERNEL_SIZE.value)
            r.append(EnumLayerParameters.INPUT_SHAPE.value)
            r.append(EnumLayerParameters.PADDING.value)
            r.append(EnumLayerParameters.ACTIVATION.value)
            return  r
        elif (enum_layer is EnumLayer.POOLING.value):
            r.append(EnumLayerParameters.POOL_SIZE.value)
            return r
        elif (enum_layer is EnumLayer.FLATTENING.value):
            return r
        else:
            return r


class EnumLoss(Enum):
    #attr = (id,name)
    MSE = ("mean_squared_error","Mean squared error")
    MAE = ("mean_absolute_error", "Mean absolute error")
    MAPE = ("mean_absolute_percentage_error", "Mean absolute percentage error")

    def getValues():
        result = []
        for data in EnumLoss:
            result.append({'id' : data[0], 'name': data[1]})
        return result

class EnumOptimizer(Enum):
    #attr = {id,name}
    SGD = ("SGD","SGD")
    RMSprop = ("RMSprop","RMSprop")
    Adadelta = ("Adadelta", "Adadelta")
    Adam = ("Adam","Adam")

    def getValues():
        result = []
        for data in EnumOptimizer:
            result.append({'id' : data[0], 'name': data[1]})
        return result

class EnumMetrics(Enum):
    #attr=(id,name)
    accuracy = ("accuracy","Accuracy")
    binary_accuracy = ("binary_accuracy","Binary accuracy")
    categorical_accuracy = ("categorical_accuracy","Categorical accuracy")
    sparse_categorical_accuracy = ("sparse_categorical_accuracy", "Sparse categorical accuracy")

    def getValues():
        result = []
        for data in EnumMetrics:
            result.append({'id' : data[0], 'name': data[1]})
        return result

def to_json():
    res = {}
    cnn = {}
    classMap,tmp = EnumLayer.getValues()
    cnn["classNames"] = tmp
    for key in classMap:
        result = []
        parameters = EnumLayerParameters.getValues(classMap[key])
        for par in parameters:
            parJson = {
                'id': par[0],
                'name': par[1],
                'expectedValue': par[2]
            }
            if (par[2] == "{}"):
                parJson['possibleValues'] = eval("Enum" + str(par[0]).capitalize()).getValues()
            result.append(parJson)
        cnn[key+"Parameters"] = result
    res['cnn'] = cnn
    return res

