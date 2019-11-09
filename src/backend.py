#!/usr/bin/env python3
from flask import Flask, request
import flask
import sys
import src.application as neuralNetworkApplication
import src.config as conf
import src.enum.enum_model_builder as el
import base64
import json
from flask_cors import CORS
import os
import binascii
from io import BytesIO
from PIL import Image
import src.enum.mlp_enum_builder as el_mlp
import src.enum.enum_model as enum_model
import threading as th

sys.path.append('db')
sys.path.append('models/cnn')
sys.path.append('models/mlp')
sys.path.append('models/genetic_alg')
sys.path.append('enum')
sys.path.append('interface')

app = Flask(__name__)
CORS(app, resources={"*": {"origins": "*"}})
# holds instance of application with neural network
application = neuralNetworkApplication.Application()
app.logger = application.log
# application.active_model.validate_model_on_test_data(application.data.test_data,application.data.test_labels)
counters = {}


### ----------------------------------###
#                                       #
#           S E R V I C E S             #
#                                       #
### ----------------------------------###

## VZOROVY POPIS SERVICE
# - input params
# - output data vo forme json
@app.route("/loadImages", methods=["POST"])
def loadImages():
    req = request.get_json()

    result = []
    # TODO: nech sa overi user, a nacitaju sa tie datasety co sa maju
    with open('dataset/main_dataset/description/metadata_all_with_X.csv', 'r') as metadata:
        data = []
        for line in metadata:
            tmp = line.split(';')
            if tmp[0] == 'name':
                continue
            data.append({'name': tmp[0] + '.jpg', 'diagnosis': tmp[0]})
        low = req.get('lastIndex')
        high = low + req.get('count')
        for i in range(low, high):
            if i > len(data):
                break
            with open('dataset/main_dataset/images/' + data[i]['name'], 'rb') as file:
                tmp = base64.b64encode(file.read())
                result.append(tmp.decode('utf-8'))
        metadata = {}
        metadata['lastIndex'] = high
        metadata['count'] = len(result)
        metadata['all'] = len(data)
        jsonData = json.dumps({'data': result, 'metadata': metadata})
        return flask.make_response(jsonData)


@app.route("/datasets", methods=["GET"])
def get_datatests():
    tmp = os.listdir('dataset')
    return flask.make_response(json.dumps(tmp))


@app.route("/predict", methods=["POST"])
def predict():
    '''
    Metoda zodpoveda signle predictu pre lognuteho/nelognuteho usera
    :param:     @AUTHORIZATION
                @PHOTO
                @MODEL_ID
    :return:    -PredictionResult.py (class)
                -PopisObrazka --> len ak je obrazok z nasho setu
    '''
    form = flask.request.get_json()
    model_id = int(form.get('model'))
    img = form.get('photo')
    auth = request.headers.get('Authorization')
    application.log.debug("EndPoint: Predict, Auth:{}, ModelId:{}".format(auth, model_id))
    jpgtxt = base64.standard_b64decode(img.split(',')[1])  # treba odrezat cestu, lebo je v otm prilozena
    dataset_name = base64.standard_b64decode(img.split(',')[0]) # cesta pre dohladanie fotky
    #TODO: dorobit tu cestu do fotky ked sa vyberie z nasich datasetov, VYSTRIHNUT DO TOHO DATASET NAME
    img = Image.open(BytesIO(jpgtxt))
    if auth is None:
        # uzivatel nebol prihlaseny, treba pouzit staticky model
        result = application.swap_active_static_model(model_id).predict_image(img)
    elif auth is not None:
        # uzivatel je prihlaseny, pouziva svoje modely
        usr = application.find_user_by_identification(auth)
        result = usr.switch_active_model(model_id).predict_image(img)
    else:
        raise Exception("Nepovolena hodnota v atribute auth! [{}]".format(auth))
    application.log.debug("Prediction result:")
    application.log.debug(result)
    return flask.make_response(json.dumps(result))


@app.route("/training-session", methods=["POST"])
def training_session():
    '''
    Metoda vrati k modelu jeho historiu trenovania
    :return:
    '''
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = form.get('modelId')
    application.log.debug("EndPoint: TrainingSession, Auth:{}, ModelId:{}".format(auth, model_id))
    file_train_session = {}
    if auth is None:
        # uzivatel nebol prihlaseny
        stat_model = application.swap_active_static_model(model_id)
        file_train_session["train_history"] = stat_model.load_train_session_file()
        file_train_session["model_info"] = stat_model.model_to_json()
        file_train_session["dataset_info"] = stat_model.ref_data.to_json()
    elif auth is not None:
        # uzivatel je prihlaseny
        usr = application.find_user_by_identification(auth)
        user_model= usr.switch_active_model(model_id)
        #file_train_session = user_model.load_train_session_file()
        if user_model.ref_data.name is None:
            file_train_session["dataset_info"] = user_model.ref_data.to_json()
        else:
            file_train_session["dataset_info"] = None
        file_train_session["train_history"] = user_model.load_train_session_file()
        file_train_session["model_info"] = user_model.model_to_json()
    else:
        raise Exception("Nepovolena hodnota v atribute auth! [{}]".format(auth))

    if file_train_session is None:
        return flask.make_response('Model este nebol trenovany',200)
    elif file_train_session is False:
        # model sa prave trenuje, treba presmerovat na live okno
        return flask.make_response('Model sa prave trenuje ', 200)
    else:
        return flask.make_response(json.dumps(file_train_session),200)

@app.route("/testing-session", methods=["POST"])
def testing_session():
    '''
    Metoda vrati k modelu jeho historiu testovania
    :return:
    '''
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = int(form.get('modelId'))
    application.log.debug("EndPoint: TestingSession, Auth:{}, ModelId:{}".format(auth, model_id))
    head_test_session_info = None
    if auth is None:
        # uzivatel nebol prihlaseny
        stat_model = application.swap_active_static_model(model_id)
        head_test_session_info = stat_model.load_test_session_file()
    elif auth is not None:
        # uzivatel je prihlaseny
        usr = application.find_user_by_identification(auth)
        user_model = usr.switch_active_model(model_id)
        if user_model.is_locked_by_training() :
            return flask.make_response("Model is locked by trainning!",200)
        elif user_model.is_trained_on_dataset()==False:
            return flask.make_response("Model has not been trained yet!", 200)
        elif user_model.ref_res_proc.test_result_path is None:
            return flask.make_response("Model has not been trained yet!", 200)
        else:
            # model bol uz trenovany, moze sa testovat
            head_test_session_info = user_model.load_test_session_file()
            if head_test_session_info is None:
                return flask.make_response("Model has not been tested yet!", 200)
    return flask.make_response(json.dumps({"testing_session": head_test_session_info}))

@app.route('/dataset/new', methods=["POST"])
def createDataset():
    data = flask.request.get_json()

    os.mkdir('dataset/' + data['name'])
    os.mkdir('dataset/' + data['name'] + '/description')
    os.mkdir('dataset/' + data['name'] + '/images')
    counters[data['name']] = 0
    keyword = 'base64,'
    position = data['metadata'].find(keyword)
    filestring = binascii.a2b_base64(data['metadata'][(position + len(keyword)):])
    with open('dataset/' + data['name'] + '/description/metadata.csv', 'wb') as file:
        file.write(filestring)

    return flask.make_response()


@app.route('/dataset/new/image', methods=["POST"])
def createImage():
    data = flask.request.get_json()
    keyword = 'base64,'
    position = data['photo']['file'].find(keyword)
    filestring = data['photo']['file'][(position + len(keyword)):]
    with open('dataset/' + data['dataset'] + '/images/' + data['photo']['name'], 'wb') as file:
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


@app.route('/models', methods=["GET"])
def get_models():
    auth = request.headers.get('Authorization')
    application.log.debug("EndPoint: GetModels, Auth:{}".format(auth))
    res = None
    if auth is None:
        # nie je lognuty, vratim staticke modely
        res = application.get_static_models()
    else:
        # je lognuty, vratim userove modely
        usr = application.find_user_by_identification(auth)
        res = usr.get_models()

    return flask.make_response(json.dumps({'models': res}, ensure_ascii=False, indent=2))


@app.route('/logout', methods=["GET"])
def logout():
    auth = request.headers.get('Authorization')
    usr = application.find_user_by_identification(auth)
    if usr is not None:
        res = application.logout_user(usr)
        if res != False:
            return flask.make_response()
    return flask.Response('Invalid identifier', 403)


@app.route('/builder', methods=['GET', 'POST'])
def builder():
    r_json = flask.request.get_json()
    if r_json is None:
        model_type = enum_model.Nn_type.CNN.value  # default
    else:
        r_json = r_json.get("modelType")
    if r_json is not None:
        if r_json == 'CNN':
            model_type =  enum_model.Nn_type.CNN.value
        elif r_json == 'MLP':
            model_type =  enum_model.Nn_type.MLP.value
        elif r_json == 'GEN':
            model_type =  enum_model.Nn_type.GEN.value
    if (request.method == 'GET'):
        return builderGetData(model_type)
    elif (request.method == 'POST'):
        return buildModel(flask.request.get_json())
    else:
        code = 404
        return flask.make_response('not found', 404)

def builderGetData(model_type):
    resJson = None
    if model_type == enum_model.Nn_type.CNN.value:
        resJson = el.to_json()
    elif model_type == enum_model.Nn_type.MLP.value:
        resJson = el_mlp.to_json()
    return flask.make_response(json.dumps((resJson)), 200)

def buildModel(jsonData):
    auth = request.headers.get('Authorization')
    if auth is not None:
        usr = application.find_user_by_identification(auth)
        if usr is not None:
            returned_model_id = usr.create_model_from_builder(jsonData)
            return flask.Response({"new_model_id": str(returned_model_id)}, 200)
    return flask.Response('Neautentifikovany user',403)

@app.route('/live_training_session', methods=["GET"])
def live_training_session():
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = form.get('model')
    application.log.debug("EndPoint: LiveTrainingSession, Auth:{}, ModelId:{}".format(auth, model_id))
    #TODO: live prediciton
    return flask.Response('este nikto nerobil', 200)


@app.route('/re_train', methods=["GET"])
def re_train():
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = form.get('model')
    application.log.debug("EndPoint: ReTrain, Auth:{}, ModelId:{}".format(auth, model_id))
    return flask.Response('este nikto nerobil', 200)

@app.route('/test', methods=["POST"])
def test():
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = int(form.get('modelId'))
    dataset_name = form.get('datasetName')
    application.log.debug("EndPoint: Test, Auth:{}, ModelId:{}".format(auth, model_id))
    res = None
    if auth is not None:
        # je niekto prihlaseny
        usr = application.find_user_by_identification(auth)
        if usr is not None:
            user_model = usr.switch_active_model(model_id)
            if dataset_name is None:
                res = user_model.test("small_dataset")
            else:
                res = user_model.test(dataset_name)
    return flask.Response(json.dumps({'results': res}, ensure_ascii=False, indent=2), 200)

@app.route('/info_models', methods=["GET"])
def show_info_models():
    '''
    Zobrazuje modelovye struktury
    :return: vrati udaje k modelovym strukturam
    '''
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = form.get('model')
    application.log.debug("EndPoint: ShowMyModels, Auth:{}, modelId: {}".format(auth,model_id))
    res_model_structure = None
    if auth is None:
        # nie je lognuty, vratim staticke modely, tie su natrenovane vzdy
        static_model = application.swap_active_static_model(model_id)
        res_model_structure = static_model.model_to_json()
    else:
        # je lognuty, zistim ci su trenovane
        usr = application.find_user_by_identification(auth)
        usr_model = usr.switch_active_model(model_id)
        if usr_model.is_locked_by_training():
            # model sa prave trenuje, to vsak nevadi, len sa presmeruje na kartu kde je progress
            res_model_structure = usr_model.model_to_json()
        elif usr_model.is_trained_on_dataset() == False:
            # este vsak nebol trenovany, inde presmerovanie
            res_model_structure = usr_model.model_to_json()
        else:
            # tu je model cely natrenovany, smeruj hned na statistiky
            res_model_structure = usr_model.model_to_json()

    return flask.Response(json.dumps(res_model_structure))

@app.route('/train', methods=["POST"])
def train():
    form = flask.request.get_json()
    auth = request.headers.get('Authorization')
    model_id = int(form.get('modelId'))
    dataset_name = form.get('datasetName')
    if dataset_name is None:
        dataset_name = "small_dataset"
    application.log.debug("EndPoint: TrainModel, Auth:{}, modelId: {}".format(auth, model_id))
    if auth is not None:
        # uzivatel je prihlaseny, mozeme dat trenovat
        usr = application.find_user_by_identification(auth)
        model = usr.switch_active_model(model_id)
        if model.is_locked_by_training():
            return flask.Response('Model is locked by training', 403)
        # oddelenie vlakna
        train_thread = th.Thread(target=model.train, args=(dataset_name,))
        train_thread.start()
        return flask.Response('OK', 200)
    else:
        md = application.swap_active_static_model(model_id)
        #md.train(dataset_name)
        return flask.Response('Forbiden for not logged user',403)

@app.route('/create-user', methods=["POST"])
def createUser():
    form = flask.request.get_json()
    username = form.get('username')
    password = form.get('password')
    application.log.debug("EndPoint: CreateUser, username:{}, password: {}".format(username, password))
    resut = application.create_user(username,password)
    if resut:
        # ok
        return flask.Response('Your account has been created. You should log in', 200)
    else:
        # nieco sa pokazilo
        return flask.Response('Something went wrong. Internal server error', 500)

@app.route('/check-user-name', methods=["GET"])
def checkUserName():
    username = request.args.get('userName')
    check_result = application.check_user_name(username)
    application.log.debug("EndPoint: ChekUserName, username:{}".format(username))
    if check_result:
        # nie je take meno, moze byt vytvoreny
        return flask.Response('OK', 200)
    else:
        # je take meno, nesmie byt vytvorene
        return flask.Response('Username already exists', 403)

## SPUSTENIE SERVERA
if __name__ == "__main__":
    application.log.debug(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(host=conf.server_host, port=conf.server_port)
