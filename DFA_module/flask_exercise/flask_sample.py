from flask import Flask, request, jsonify, make_response
import json_length

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route("/json", methods = ["POST"])
def json_sample():

    if request.is_json:

        req = request.get_json() #json to dict

        length = json_length.json_length(req)

        response_body = {
            "original json": req,
            "length": length
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:
        
        return make_response(jsonify({"original json": "Request was not JSON", "length": -1}), 400)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
