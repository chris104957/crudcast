from datetime import datetime
from exceptions import ValidationError
from pymongo.collection import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import NotFound


class BaseField(object):
    auto = False

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

    def set(self, created=False):
        """
        This method must be extended by all child classes. If it returns None, the value will not be changed

        :param created: determines whether or not the object is being created or updated
        """
        raise NotImplementedError()

    def validate(self, data, _id=None):
        raise ValidationError('Auto fields cannot be set manually', field=self.name)


class StringField(BaseField):
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

    def set(self, created=False):
        """
        Returns the collection length + 1 when the object is created
        """
        if created:
            return self.model.collection.find().count() + 1


class BooleanField(BaseField):
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
    @staticmethod
    def get_related(related_model_name):
        from models import Model
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
            raise ValidationError('Cannot find %s with that ID' % self.related.name, field=self.name)

        return data
