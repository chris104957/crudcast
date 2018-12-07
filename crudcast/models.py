from .utils import get_models, is_jsonable
from .exceptions import ValidationError
from pymongo.collection import ObjectId
from .fields import (
    StringField, NumberField, DateTimeField, BooleanField, ForeignKeyField, AutoField, AutoDateTimeField,
    ManyToManyField
)
from flask import abort


models = get_models()


class Model(object):
    def __init__(self, name):
        """
        A model object - effectively a schema for the mongodb

        :param name: model name
        """
        self.name = name
        try:
            self.object = models[name]
        except KeyError:
            abort(404)
        self.collection = self.object['collection']
        self.fields = self.set_fields(self.object['fields'])
        self.options = self.object.get('options', {})

    def set_fields(self, fields):
        """
        Sets the list of fields
        """
        cleaned_fields = []
        field_types = {
            'string': StringField,
            'number': NumberField,
            'datetime': DateTimeField,
            'boolean': BooleanField,
            'foreignkey': ForeignKeyField,
            'autofield': AutoField,
            'auto_datetime': AutoDateTimeField,
            'manytomany': ManyToManyField
        }

        for field_name, options in fields.items():
            if not options:
                options = {}

            field_type = field_types[options.get('type', 'string')]

            field = field_type(name=field_name, model=self, **options)

            cleaned_fields.append(field)

        return cleaned_fields

    @property
    def fieldnames(self):
        return [field.name for field in self.fields]

    def get_field_by_name(self, key):
        return list(filter(lambda x: x.name == key, self.fields))[0]

    def validate(self, data=None, _id=None):
        # prevent 500 error on empty payload
        if not data:
            data = {}

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
            field.validate(val, _id=_id)

        auto_fields = [field for field in self.fields if field.auto]

        for f in auto_fields:
            data[f.name] = f.set(_id=_id)

        return data

    def find(self, **query):
        q = {}
        for key, val in query.items():
            try:
                q[key] = ''.join(val)
            except TypeError:
                q[key] = val
        return self.collection.find(q)

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

    def retrieve(self, _id):
        if self.exists(_id):
            return self.to_repr(_id=ObjectId(_id))[0]
        else:
            abort(404)

    def create(self, data):
        data = self.validate(data)
        obj = self.collection.insert_one(data)
        return self.retrieve(obj.inserted_id)

    def update(self, _id, data):
        if not self.exists(_id):
            abort(404)

        data = self.validate(data, _id=_id)
        self.collection.find_one_and_update({'_id': ObjectId(_id)}, {'$set': data})
        return self.retrieve(_id)

    def exists(self, _id):
        """
        Check to see if a document with a given ID exists

        :param _id: the id to check
        :type _id: str
        :rtype: bool
        """
        return self.collection.find({'_id': ObjectId(_id)}).count() == 1

    def delete(self, _id):
        if self.exists(_id):
            self.collection.find_one_and_delete({'_id': ObjectId(_id)})
            return {}
        else:
            abort(404)
