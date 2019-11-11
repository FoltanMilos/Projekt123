from enum import Enum

class EnumLayer(Enum):
    LAYER = "Layer"

    @staticmethod
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

    @staticmethod
    def getValues():
            result = []
            for data in EnumActivation:
                result.append({"id": data.name, "name": data.value})
            return result

class EnumLayerParameters(Enum):
    #attr = tuple(ID,display_name, ExpectedVale)
    NAME = ("NAME","name","string")
    NEURON_COUNT = ("NEURON_COUNT","neuron count", "number")
    @staticmethod
    def getValues(enum_layer):
        values = [item.value for item in EnumLayer]
        if (not enum_layer in values):
            raise Exception('must be member of EnumLayers')
        r = []
        r.append(EnumLayerParameters.NAME.value)
        if(enum_layer is EnumLayer.LAYER.value):
            r.append(EnumLayerParameters.NEURON_COUNT.value)
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
    mlp['activation'] = EnumActivation.getValues()
    res['mlp'] = mlp
    return res