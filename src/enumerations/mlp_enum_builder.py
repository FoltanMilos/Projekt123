from enum import Enum

class EnumLayer(Enum):
    LAYER = "Layer"
    PARAMS = "Params"

    @staticmethod
    def getValues():
        map = {}
        classNames = []
        for data in EnumLayer:
            map[data.name] =  data.value
            classNames.append({'id' : data.name, 'name': data.value})
        return map,classNames

class EnumLayerParameters(Enum):
    #attr = tuple(ID,display_name, ExpectedVale)
    NEURON_COUNT = ("NEURON_COUNT","neuron count", "number")
    ACTIVATION_FUNCTION = ("ACTIVATION_FUNCTION","activation function", "string")
    LEARNING_RATE = ("LEARNING_RATE","learning rate", "number")
    EPSILON = ("EPSILON","epsilon", "number")
    @staticmethod
    def getValues(enum_layer):
        values = [item.value for item in EnumLayer]
        if (not enum_layer in values):
            raise Exception('must be member of EnumLayers')
        r = []
        if(enum_layer is EnumLayer.LAYER.value):
            r.append(EnumLayerParameters.NEURON_COUNT.value)
            r.append(EnumLayerParameters.ACTIVATION_FUNCTION.value)
        elif enum_layer is EnumLayer.PARAMS.value:
            r.append(EnumLayerParameters.LEARNING_RATE.value)
            r.append(EnumLayerParameters.EPSILON.value)
        return r

def to_json():
    res = {}
    mlp = {}
    classMap,tmp = EnumLayer.getValues()
    mlp["classNames"] = tmp
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
        mlp[key+"Parameters"] = result
    res['mlp'] = mlp
    return res
