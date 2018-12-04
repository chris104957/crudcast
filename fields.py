from exceptions import ValidationError
from datetime import datetime
from models import Model


class BaseField(object):
    def __init__(self, name, model, **options):
        """
        Base field object.

        :param name: Field name.
        :param model: the Model object to which the field belongs
        :type model: `models.Model`
        :param options: field options. The available options vary based on field type. Only the `required` option is
        implemented at this level

        # TODO: enforce no spaces in in the field name
        # TODO: validate that the field name is unique for the current model
        """
        self.name = name
        self.model = model
        self.required = options.get('required', False)

    def validate(self, data):
        raise NotImplementedError()


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
        self.unique = options.get('unique', False)

    def validate(self, data):
        """
        Validates that the input value is a string, and performs uniqueness checking if required
        """
        if self.unique:
            # TODO: implement this. Look for matching objects in the collection, and raise an error if one is found
            pass

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

    def validate(self, data):
        try:
            datetime.strptime(data, self.format_string)
        except ValueError as err:
            raise ValidationError(err, field=self.name)
        return data


class NumberField(BaseField):
    """
    Numeric input field.
    """
    def validate(self, data):
        try:
            assert isinstance(data, (int, float, complex))
        except AssertionError:
            raise ValidationError('Input must be numeric', field=self.name)

        return data


class BooleanField(BaseField):
    def validate(self, data):
        """
        Checks that the input value is a Boolean
        """
        try:
            assert data in [True, False]
        except AssertionError:
            raise ValidationError('Input must be true or false', field=self.name)
        return data


class ForeignKeyField(BaseField):
    @staticmethod
    def get_related(related_model_name):
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

    def validate(self, data):
        """
        Checks to see if a document in the related model's collection matches the ID provided as `data`

        :param data: the valid ID of a document, as a string
        """
        try:
            self.related.retrieve(data)
        except:
            # TODO: update the above line to catch a specific error
            raise ValidationError('Unable to find a %s document with that id' % self.related.name, field=self.name)

        return data
