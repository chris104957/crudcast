from datetime import datetime
from .exceptions import ValidationError
from pymongo.collection import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import NotFound


class BaseField(object):
    auto = False
    type = ''

    def __init__(self, name, model, **options):
        """
        Base field object.

        :param name: Field name.
        :param model: the Model object to which the field belongs
        :type model: `models.Model`
        :param options: field options. The available options vary based on field type. Only the `required` and
        `unique` options are implemented at this level
        """
        self.name = name
        self.model = model
        self.required = options.get('required', False)
        self.unique = options.get('unique', False)

    def validate(self, data, _id=None):
        if self.unique:
            query = {self.name: data}
            if _id:
                """
                If object is being updated, the query is adjusted to exclude the object being updated (otherwise, 
                it isn't possible to save an object without changing the unique field values every time)
                """
                query['_id'] = {'$not': {'$eq': ObjectId(_id)}}

            if self.model.collection.find(query).count() > 0:
                raise ValidationError('%s with this %s already exists' % (self.model.name, self.name),
                                      field=self.name)
        return data


class AutoBaseField(BaseField):
    """
    An automatically generated field. When `Model.create()` is called, the fields will be set automatically - the
    `.set()` method must be implemented in order for this to happen. Any attempt to set the value of this field
    manually will generate a ValidationError
    """
    auto = True

    def get_original(self, _id):
        """
        Helper function that returns the original value of the object, before it is updated. If you want to leave a
        value unchanged on update, the `.set()` method should call and return this function (otherwise the field
        value will be set to `None`)

        :param _id: the object id as a string
        """
        obj = self.model.to_repr(_id=ObjectId(_id))[0]
        return obj[self.name]

    def set(self, _id=None):
        """
        This method must be extended by all child classes. If it returns None, the value will not be changed

        :param _id: If an object is being updated, the _id will be provided
        """
        raise NotImplementedError()

    def validate(self, data, _id=None):
        raise ValidationError('Auto fields cannot be set manually', field=self.name)


class StringField(BaseField):
    type = 'string'

    def __init__(self, name, **options):
        """
        String input field

        :param name: field name
        :param unique: if True, no new documents can be created if there is another document in the collection has
        the same value for this field as the one being provided
        :type unique: Boolean
        """
        super(StringField, self).__init__(name, **options)

    def validate(self, data, _id=None):
        """
        Validates that the input value is a string, and performs uniqueness checking if required
        """
        data = super().validate(data, _id=_id)
        try:
            assert isinstance(data, str)
        except AssertionError:
            raise ValidationError('Input must be a string', field=self.name)

        return data


class DateTimeField(BaseField):
    def __init__(self, name, **options):
        """
        A field for storing datetime objects

        :param name: field name
        :param format_string: format string to be used for validating input. Defaults to '%Y-%m-%d %H:%M:%S.%f' (ISO
        format)
        """
        self.format_string = options.get('format_string', '%Y-%m-%d %H:%M:%S.%f')
        super(DateTimeField, self).__init__(name, **options)

    def validate(self, data, _id=None):
        data = super().validate(data, _id=_id)
        try:
            datetime.strptime(data, self.format_string)
        except ValueError as err:
            raise ValidationError(err, field=self.name)
        return data


class NumberField(BaseField):
    """
    Numeric input field.
    """

    type = 'number'

    def validate(self, data, _id=None):
        data = super().validate(data, _id=_id)
        try:
            assert isinstance(data, (int, float, complex))
        except AssertionError:
            raise ValidationError('Input must be numeric', field=self.name)

        return data


class AutoField(AutoBaseField):
    """
    An auto field, e.g. one that creates a sequential number, e.g. 1, 2, 3, etc. Cannot be set manually - fields that
    extend this must implement the `.set()` method
    """

    def set(self, _id=None):
        """
        Returns the collection length + 1 when the object is created
        """
        if _id:
            return self.get_original(_id)
        else:
            return self.model.collection.find().count() + 1


class AutoDateTimeField(AutoBaseField):
    def __init__(self, name, model, **options):
        """
        Automatically populates the current time at the moment of saving the object. If `create_only` is `True`,
        then the field only gets set when the document is created
        """
        super(AutoDateTimeField, self).__init__(name, model, **options)
        self.create_only = options.get('create_only', False)

    def set(self, _id=None):
        if not self.create_only or not _id:
            return datetime.utcnow()
        else:
            return self.get_original(_id)


class BooleanField(BaseField):
    type = 'boolean'

    def validate(self, data, _id=None):
        """
        Checks that the input value is a Boolean
        """
        data = super().validate(data, _id=_id)
        try:
            assert data in [True, False]
        except AssertionError:
            raise ValidationError('Input must be true or false', field=self.name)
        return data


class ForeignKeyField(BaseField):
    type = 'object'

    @staticmethod
    def get_related(related_model_name):
        from .models import Model
        return Model(name=related_model_name)

    def __init__(self, name, model, **options):
        """
        A field that points at another collection in the database

        :param name: field name
        :param model: parent model
        :param to:  the related model's name
        """
        super(ForeignKeyField, self).__init__(name, model, **options)
        self.related = self.get_related(options['to'])

    def validate(self, data, _id=None):
        """
        Checks to see if a document in the related model's collection matches the ID provided as `data`
        """
        data = super().validate(data, _id=_id)
        try:
            self.related.retrieve(data)
        except InvalidId:
            raise ValidationError('Invalid id', field=self.name)
        except NotFound:
            raise ValidationError('Cannot find %s with ID %s' % (self.related.name, data), field=self.name)

        return data


class ManyToManyField(ForeignKeyField):
    type = 'array'

    def validate(self, data, _id=None):
        """
        Checks to see if a document in the related model's collection matches the ID provided as `data`
        """
        for d in data:
            super().validate(d, _id=_id)

        return data
