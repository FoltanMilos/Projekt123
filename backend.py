from flask import Flask,request
import flask
#import application as neuralNetworkApplication
import nn_type
import base64
import json
from flask_cors import CORS
import csv

# server application instance
app = Flask(__name__)
CORS(app, resources={"*": {"origins": "*"}})
# holds instance of application with neural network
#application = neuralNetworkApplication.Application(True)




### ----------------------------------###
#                                       #
#           S E R V I C E S             #
#                                       #
### ----------------------------------###

## VZOROVY POPIS SERVICE
# - input params
# - output data vo forme json
@app.route("/loadImages",methods=["POST"])
def loadImages():
    req = request.get_json()
    
    result = []
    with open('dataset/cnn/description/metadata.csv','r') as metadata:
        data = []
        for line in metadata:
            tmp = line.split(';')
            if tmp[0] == 'name':
                continue
            data.append({'name': tmp[0]+'.jpg', 'diagnosis': tmp[0]})
        low = req.get('lastIndex')
        high = low + req.get('count') 
        for i in range(low, high):
            if i > len(data):
                break
            with open('dataset/cnn/images/'+data[i]['name'], 'rb') as file:
                tmp = base64.b64encode(file.read())
                result.append(tmp.decode('utf-8'))
        metadata = {}
        metadata['lastIndex'] = high
        metadata['count'] = len(result)
        metadata['all'] = len(data)
        jsonData = json.dumps({'data': result,'metadata': metadata})
        return flask.make_response(jsonData)
#    with open('dataset/cnn/images/ISIC_0024306.jpg', 'rb') as file:
#         tmp = base64.b64encode(file.read())
#         result.append(tmp.decode('utf-8'))

#     with open('dataset/cnn/images/ISIC_0024307.jpg', 'rb') as file:
#         tmp = base64.b64encode(file.read())
#         result.append(tmp.decode('utf-8'))
#         


@app.route("/predict",methods=["POST"])
def predict():
    returnData = {
        "succes" : True,
        "result" : -999
                  }

    if flask.request.method == "POST":
        ppp = application.predict()
    else:
        returnData["succes"] = False

    return flask.jsonify(returnData)


# with open('dataset/cnn/images/ISIC_0024306.jpg', 'rb') as file:
#     tmp =  base64.b64encode(file.read())
#     tmp = tmp.decode('utf-8')
#     res = json.dumps(tmp)
#     print(res)

## SPUSTENIE SERVERA
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(host=0000, port=8000)
