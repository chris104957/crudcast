from flask import Flask, jsonify, request
from models import Model
from exceptions import ValidationError
from utils import get_config, _

config = get_config()
app = Flask(__name__)


@app.route('/%s/<string:model_name>/' % _('base_path'), methods=['GET'])
def list_object(model_name):
    model = Model(model_name)
    return jsonify(model.to_repr())


@app.route('/%s/<string:model_name>/' % _('base_path'), methods=['POST'])
def create_object(model_name):
    model = Model(model_name)
    response = model.create(request.json)
    return jsonify(response)


@app.route('/%s/<string:model_name>/<string:id>/' % _('base_path'), methods=['GET'])
def retrieve_object(model_name, id):
    model = Model(model_name)
    response = model.retrieve(id)
    return jsonify(response)


@app.route('/%s/<string:model_name>/<string:id>/' % _('base_path'), methods=['PUT'])
def update_object(model_name, id):
    model = Model(model_name)
    response = model.update(id=id, data=request.json)
    return jsonify(response)


def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.register_error_handler(ValidationError, handle_invalid_usage)
    app.run()
