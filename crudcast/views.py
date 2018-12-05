from flask import Flask, jsonify, request
from flask_restplus import Resource, Api

from models import Model
from exceptions import ValidationError
from utils import get_config, get_config_option


config = get_config()
app = Flask('crudcast')
api = Api(app)


@api.route('/%s/<string:model_name>/' % get_config_option('base_path'))
class ModelView(Resource):
    def get(self, model_name):
        model = Model(model_name)
        return model.to_repr()

    def post(self, model_name):
        model = Model(model_name)
        response = model.create(request.json)
        return response

# #
# #
# # @app.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['GET'])
# # def retrieve_object(model_name, _id):
# #     model = Model(model_name)
# #     response = model.retrieve(_id)
# #     return jsonify(response)
# #
# #
# # @app.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['PUT'])
# # def update_object(model_name, _id):
# #     model = Model(model_name)
# #     response = model.update(_id=_id, data=request.json)
# #     return jsonify(response)
# #
# #
# # @api.route('/%s/<string:model_name>/<string:_id>/' % get_config_option('base_path'), methods=['DELETE'])
# # def delete_object(model_name, _id):
# #     model = Model(model_name)
# #     response = model.delete(_id=_id)
# #     return jsonify(response), 204


def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


app.register_error_handler(ValidationError, handle_invalid_usage)

if __name__ == '__main__':
    app.run(debug=True)
