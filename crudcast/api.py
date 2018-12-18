from flask_restplus import Api
from crudcast.resources import ModelResource, InstanceResource, UserModelResource, UserInstanceResource


def get_api(app):
    base_path = app.crudcast_config['swagger']['basePath']
    api = Api(app, doc=False)

    mr = ModelResource
    mr.set_app(app)

    ir = InstanceResource
    ir.set_app(app)

    api.add_resource(mr, '%s/<string:model_name>/' % base_path)
    api.add_resource(ir, '%s/<string:model_name>/<string:_id>/' % base_path)

    for path, method in app.methods.items():
        resource = method.get_resource()
        resource.set_app(app)
        api.add_resource(resource, '%s/%s' % (base_path, path))

    if app.user_manager:
        umr = UserModelResource
        umr.set_app(app)

        uir = UserInstanceResource
        uir.set_app(app)

        api.add_resource(umr, '%s/user/' % app.crudcast_config['swagger']['basePath'])
        api.add_resource(uir, '%s/user/<string:_id>/' % app.crudcast_config['swagger']['basePath'])



