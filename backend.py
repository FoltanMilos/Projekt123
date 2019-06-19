import flask
import application as neuralNetworkApplication
import nn_type

# server application instance
app = flask.Flask(__name__)

# holds instance of application with neural network
application = neuralNetworkApplication.Application(False,nn_type.Nn_type.CNN)




### ----------------------------------###
#                                       #
#           S E R V I C E S             #
#                                       #
### ----------------------------------###

## VZOROVY POPIS SERVICE
# - input params
# - output data vo forme json
@app.route("/loadImage",methods=["GET","POST"])
def loadImage():
    returnData = {"success": True}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            pass

    return flask.jsonify(returnData)



## SPUSTENIE SERVERA
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(host=0000, port=8000)
