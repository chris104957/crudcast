from flask_restplus import Api
from .resources import ModelResource, InstanceResource
from flask import send_file


def send_js():
    return send_file('swagger.json')


def get_api(app):
    api = Api(app, doc=False)
    api.add_resource(ModelResource, '%s/<string:model_name>/' % app.crudcast_config['swagger']['basePath'])
    api.add_resource(InstanceResource, '%s/<string:model_name>/<string:_id>/' % app.crudcast_config['swagger']['basePath'])



