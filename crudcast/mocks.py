from crudcast.resources import Resource


class MockApi(object):
    pass


class MockCollection(object):
    items = []

    def find(self, query):
        return MockDocument(_count=self.count)

    def insert_one(self, *args, **kwargs):
        d = MockDocument()
        self.items.append(d)
        return d

    def __init__(self, *args, **kwargs):
        self.count = kwargs.get('count', 0)


class MockMethod(object):
    def __init__(self, *args, **kwargs):
        pass


class MockApp(object):
    user_manager = None
    handle_exception = None
    handle_user_exception = None
    methods = {}

    def run(self, *args, **kwargs):
        pass

    extensions = {}
    config = {}
    crudcast_config = {
        'swagger': {
            'basePath': 'api'
        }
    }
    models = {
        'test': {
            'collection': MockCollection(),
            'fields': {}
        }
    }

    def route(self, *args, **kwargs):
        return lambda x: print(x)

    def register_blueprint(self, *args, **kwargs):
        pass

    def register_error_handler(self, *args, **kwargs):
        pass

    @classmethod
    def add_url_rule(rule, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        pass

    def get_swagger_ui_view(self, *args, **kwargs):
        pass


class MockArgs(object):
    config_file = 'something invalid'
    import_name = 'Crudcast'
    port = 5000
    debug = False
    host = '0.0.0.0'
    no_load_dotenv = False
    create_admin = False


class MockParser(object):
    def parse_args(self):
        return MockArgs

    def add_argument(self, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        pass


class MockDocument(object):
    _count = 0

    def items(self):
        return [{'test': 'test'}]

    def __init__(self, *args, **kwargs):
        self._count = kwargs.get('_count', 0)

    def __iter__(self):
        for item in self.items():
            yield item

    def count(self):
        return self._count

    inserted_id = '507f1f77bcf86cd799439011'


class MockModel(object):
    models = ['test', 'test2']
    count = 0
    name = None
    app = MockApp()

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.count = kwargs.get('count', 0)
        self.collection = MockCollection(count=self.count)
        pass

    def to_repr(self, _id):
        return [{
            'test': {}
        }]


class MockValidationError(Exception):
    pass


class MockMongo(object):
    def __getitem__(self, item):
        return {
            'test': MockCollection(),
            'test2': MockCollection(),
        }

    def __init__(self, *args, **kwargs):
        pass


class TestResource(Resource):
    def get(self):
        return {'hello': True}