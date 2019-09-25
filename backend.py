from flask import Flask,request
import flask
import application as neuralNetworkApplication
import nn_type
import base64
import json
from flask_cors import CORS
import csv
import os
import binascii
import config
import model_builder_enums as el;

# server application instance
app = Flask(__name__)
CORS(app, resources={"*": {"origins": "*"}})
# holds instance of application with neural network
application = neuralNetworkApplication.Application(config.load_model)
#application.active_model.validate_model_on_test_data(application.data.test_data,application.data.test_labels)
counters = {}

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
    with open('dataset/main_dataset/description/metadata.csv','r') as metadata:
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
            with open('dataset/main_dataset/images/'+data[i]['name'], 'rb') as file:
                tmp = base64.b64encode(file.read())
                result.append(tmp.decode('utf-8'))
        metadata = {}
        metadata['lastIndex'] = high
        metadata['count'] = len(result)
        metadata['all'] = len(data)
        jsonData = json.dumps({'data': result,'metadata': metadata})
        return flask.make_response(jsonData)
#    with open('dataset/main_dataset/images/ISIC_0024306.jpg', 'rb') as file:
#         tmp = base64.b64encode(file.read())
#         result.append(tmp.decode('utf-8'))

#     with open('dataset/main_dataset/images/ISIC_0024307.jpg', 'rb') as file:
#         tmp = base64.b64encode(file.read())
#         result.append(tmp.decode('utf-8'))
#         


@app.route("/predict",methods=["POST"])
def predict():
    form = flask.request.get_json()
    image = form.get('photo')
    
    return flask.make_response()

@app.route("/train", methods=["POST"])
def train(): 
    form = flask.request.get_json()
    print(form.get('useDataset'))
    return flask.make_response()

@app.route('/dataset/new',methods=["POST"])
def createDataset():
    data = flask.request.get_json()

    os.mkdir('dataset/'+data['name'])
    os.mkdir('dataset/'+data['name']+'/description')
    os.mkdir('dataset/'+data['name']+'/images')
    counters[data['name']] = 0
    keyword = 'base64,'
    position = data['metadata'].find(keyword)
    filestring = binascii.a2b_base64(data['metadata'][(position + len(keyword)):])
    with open('dataset/'+data['name']+'/description/metadata.csv','wb') as file:
        file.write(filestring)
    
    return flask.make_response()

@app.route('/dataset/new/image', methods=["POST"])
def createImage():
    data = flask.request.get_json()
    keyword = 'base64,'
    position = data['photo']['file'].find(keyword)
    filestring = data['photo']['file'][(position + len(keyword)):]
    with open('dataset/'+data['dataset']+'/images/'+data['photo']['name'],'wb') as file:
        file.write(binascii.a2b_base64(filestring))
    counters[data['dataset']] += 1
    
    return flask.make_response()

@app.route('/login', methods=["POST"])
def login():
    data = flask.request.get_json()
    res = application.validate_user(data)
    if res == False:
        return flask.Response('invalid credentials', 401)
    else:
        return flask.make_response(json.dumps(res))
# with open('dataset/main_dataset/images/ISIC_0024306.jpg', 'rb') as file:
#     tmp =  base64.b64encode(file.read())
#     tmp = tmp.decode('utf-8')
#     res = json.dumps(tmp)
#     print(res)

@app.route('/models', methods=["GET"])
def get_models():
    auth = request.headers.get('Authorization')
    usr = application.find_user_by_identification(auth)
    if(usr != False):
        res = application.get_models(usr)
        return flask.make_response(json.dumps({'models': res},ensure_ascii=False,indent=2))
    return flask.Response('Access Denied', 403)


@app.route('/logout', methods=["GET"])
def logout():
    auth = request.headers.get('Authorization')
    usr = application.find_user_by_identification(auth)
    if(usr != False):
        res = application.logout_user(usr)
        if res != False:
            return flask.make_response()
    return flask.Response('Invalid identifier', 403)

@app.route('/modelBuilder',methods=['GET'])
def modelBuilder():
    lay = el.EnumLayer.DENSE
    ll = el.EnumLayerParameters.getValues(lay)
    print(ll)
    return flask.make_response('modelBuilderExample',200)





## SPUSTENIE SERVERA
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(host=0000, port=8000)
