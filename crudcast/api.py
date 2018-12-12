from flask_restplus import Api
from crudcast.resources import ModelResource, InstanceResource, UserModelResource, UserInstanceResource


def get_api(app):
    api = Api(app, doc=False)

    mr = ModelResource
    mr.set_app(app)

    ir = InstanceResource
    ir.set_app(app)

    api.add_resource(mr, '%s/<string:model_name>/' % app.crudcast_config['swagger']['basePath'])
    api.add_resource(ir, '%s/<string:model_name>/<string:_id>/' % app.crudcast_config['swagger']['basePath'])

    if app.user_manager:
        umr = UserModelResource
        umr.set_app(app)

        uir = UserInstanceResource
        uir.set_app(app)

        api.add_resource(umr, '%s/user/' % app.crudcast_config['swagger']['basePath'])
        api.add_resource(uir, '%s/user/<string:_id>/' % app.crudcast_config['swagger']['basePath'])



