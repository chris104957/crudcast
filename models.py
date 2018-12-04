from utils import get_models, _, is_jsonable
from exceptions import ValidationError
from pymongo.collection import ObjectId
models = get_models()


class BaseField(object):
    def __init__(self, name, **options):
        self.name = name
        self.required = options.get('required', False)

    def validate(self, data):
        raise NotImplementedError()


class StringField(BaseField):
    def validate(self, data):
        try:
            assert isinstance(data, str)
        except AssertionError:
            raise ValidationError('Input must be a string', field=self.name)

        return data


class NumberField(BaseField):
    def validate(self, data):
        try:
            assert isinstance(data, (int, float, complex))
        except AssertionError:
            raise ValidationError('Input must be numeric', field=self.name)

        return data


class Model(object):
    def __init__(self, name):
        self.object = models[name]
        self.collection = self.object['collection']
        self.fields = self.set_fields(self.object['fields'])

    def set_fields(self, fields):
        cleaned_fields = []
        field_types = {
            'string': StringField,
            'number': NumberField
        }

        for field_name, options in fields.items():
            if not options:
                options = {}

            field_type = field_types[options.get('type', 'string')]

            field = field_type(name=field_name, **options)

            cleaned_fields.append(field)

        return cleaned_fields

    @property
    def fieldnames(self):
        return [field.name for field in self.fields]

    def get_field_by_name(self, key):
        return list(filter(lambda x: x.name == key, self.fields))[0]

    def validate(self, data):
        # ensure that required fields are supplied
        required_fields = [field.name for field in self.fields if field.required]
        for f in required_fields:
            try:
                assert f in data.keys()
            except AssertionError:
                raise ValidationError('This field is required', field=f)

        # ensure that all input fields are valid field names
        for key, val in data.items():
            if not key in self.fieldnames:
                raise ValidationError('Invalid field', field=key)

            # perform field-level validation
            field = self.get_field_by_name(key)
            field.validate(val)

        return data

    def find(self, **query):
        return self.collection.find(query)

    def to_repr(self, **query):
        items = self.find(**query)
        response = []
        for item in items:
            obj = {}
            for key, val in item.items():
                if is_jsonable(val):
                   obj[key] = val
                else:
                    obj[key] = str(val)

            response.append(obj)

        return response

    def retrieve(self, id):
        return self.to_repr(_id=ObjectId(id))[0]

    def create(self, data):
        data = self.validate(data)
        obj = self.collection.insert_one(data)
        return self.retrieve(obj.inserted_id)

    def update(self, id, data):
        data = self.validate(data)
        self.collection.find_one_and_update({'_id': ObjectId(id)}, {'$set': data})
        return self.retrieve(id)


