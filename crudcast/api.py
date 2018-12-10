from flask_restplus import Api
from .resources import ModelResource, InstanceResource
from flask import send_file


def send_js():
    return send_file('swagger.json')


def get_api(app):
    api = Api(app, doc=False)

    mr = ModelResource
    mr.set_app(app)

    ir = InstanceResource
    ir.set_app(app)

    api.add_resource(mr, '%s/<string:model_name>/' % app.crudcast_config['swagger']['basePath'])
    api.add_resource(ir, '%s/<string:model_name>/<string:_id>/' % app.crudcast_config['swagger']['basePath'])



