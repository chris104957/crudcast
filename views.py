from flask import Flask, jsonify, request
from models import Model
from exceptions import ValidationError
from utils import get_config, get_config_option

config = get_config()
app = Flask(__name__)


@app.route('/%s/<string:model_name>/' % get_config_option('base_path'), methods=['GET'])
def list_object(model_name):
    model = Model(model_name)
    return jsonify(model.to_repr())


@app.route('/%s/<string:model_name>/' % get_config_option('base_path'), methods=['POST'])
def create_object(model_name):
    model = Model(model_name)
    response = model.create(request.json)
    return jsonify(response), 201


@app.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['GET'])
def retrieve_object(model_name, _id):
    model = Model(model_name)
    response = model.retrieve(_id)
    return jsonify(response)


@app.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['PUT'])
def update_object(model_name, _id):
    model = Model(model_name)
    response = model.update(_id=_id, data=request.json)
    return jsonify(response)


@app.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['DELETE'])
def delete_object(model_name, _id):
    model = Model(model_name)
    response = model.delete(_id=_id)
    return jsonify(response), 204


def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


app.register_error_handler(ValidationError, handle_invalid_usage)
app.run()
