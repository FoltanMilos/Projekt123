import flask
import application as neuralNetworkApplication
import nn_type
import base64
import json
from flask_cors import CORS
import csv

# server application instance
app = flask.Flask(__name__)
CORS(app)
# holds instance of application with neural network
application = neuralNetworkApplication.Application(True)




### ----------------------------------###
#                                       #
#           S E R V I C E S             #
#                                       #
### ----------------------------------###

## VZOROVY POPIS SERVICE
# - input params
# - output data vo forme json
@app.route("/loadImage",methods=["POST"])
def loadImages():
    result = []
    with open('images_other/description(MSK-1)/metadata.csv','r') as metadata:
        reader = csv.reader(metadata)
        data = []
        for row in reader:
            data.append({'name': row[0], 'diagnosis': row[0]})

        req = flask.request.data['metadata']
    with open('dataset/cnn/images/ISIC_0024306.jpg', 'rb') as file:
        tmp = base64.b64encode(file.read())
        result.append(tmp.decode('utf-8'))

    with open('dataset/cnn/images/ISIC_0024307.jpg', 'rb') as file:
        tmp = base64.b64encode(file.read())
        result.append(tmp.decode('utf-8'))
        jsonData = json.dumps({'data': result})
    return flask.make_response(jsonData)


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
