import importlib.util


class Method(object):
    def __init__(self, file, path, resource, **options):
        self.file = file
        self.path = path
        self.code = resource
        self.options = options

    def get_resource(self):
        _cls = self.code.split('.')[-1]
        spec = importlib.util.spec_from_file_location(self.code, self.file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, _cls)

    @property
    def swagger_definition(self):
        extra_swagger = self.options.get('swagger', {})

        res = self.get_resource()
        auth_type = self.options.get('auth_type')
        swagger = {}

        get = getattr(res, 'get', None)
        post = getattr(res, 'post', None)
        put = getattr(res, 'put', None)
        delete = getattr(res, 'delete', None)

        obj = {
                'tags': [self.code],
                'summary': 'Custom function',
                'consumes': 'application/json',
                'produces': 'application/json',
                'responses': {
                    '200': {
                        'description': 'successful operation',
                    }
                },
                'security': [
                    {
                        'basicAuth': []
                    }
                ] if auth_type else []
            }

        if get:
            swagger['get'] = obj
            for key, val in extra_swagger.get('get', {}).items():
                obj[key] = val
        if post:
            swagger['post'] = obj
            for key, val in extra_swagger.get('post', {}).items():
                obj[key] = val
        if put:
            swagger['put'] = obj
            for key, val in extra_swagger.get('put', {}).items():
                obj[key] = val
        if delete:
            swagger['delete'] = obj
            for key, val in extra_swagger.get('delete', {}).items():
                obj[key] = val

        return swagger


