import unittest
import mock
from mocks import MockApi, MockApp, MockParser, MockModel
from fields import (
    BaseField, AutoBaseField, StringField, DateTimeField, NumberField, AutoField, AutoDateTimeField, BooleanField,
    ForeignKeyField
)
from models import Model
from api import get_api
from app import CrudcastApp
import json
from datetime import datetime


crudcast_config = {
    'models': {
        'test': {
            'fields': {
                'm2m': {
                    'type': 'manytomany',
                    'to': 'test2'
                },
                'name': {
                    'type': 'string',
                    'unique': True,
                    'required': True
                }
            }
        },
        'test2': {}
    },
    'something_else': None
}


class CrudCastTestCase(unittest.TestCase):
    @mock.patch('flask_restplus.Api', MockApi)
    def test_api(self, *args):
        get_api(MockApp)

    def test_app(self, *args):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(crudcast_config))):
            app = CrudcastApp(__name__, config_file='file')
            self.assertEqual(app.swagger_config['swagger'], '2.0')

            with mock.patch('flask_swagger_ui.get_swaggerui_blueprint'):
                app.get_swagger_ui_view()

    @mock.patch('crudcast.app.CrudcastApp', MockApp)
    @mock.patch('argparse.ArgumentParser', MockParser)
    def test_entrypoint(self, *args):
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(crudcast_config))):
            from entrypoint import main
            main()

    def test_exceptions(self, *args,):
        from crudcast.exceptions import handle_invalid_usage, ValidationError
        with self.assertRaises(RuntimeError):
            handle_invalid_usage(ValidationError('test', status_code=415))

    def test_fields(self):
        f = BaseField(name='test', model=MockModel(), unique=True)
        data = f.validate(data=None, _id='507f1f77bcf86cd799439011')
        self.assertIsNone(data)

        model = MockModel(count=10)

        with self.assertRaises(Exception):
            f = BaseField(name='test', model=model, unique=True)
            f.validate(data=None, _id='507f1f77bcf86cd799439011')

        f = AutoBaseField(name='test', model=MockModel())
        f.get_original('507f1f77bcf86cd799439011')

        with self.assertRaises(NotImplementedError):
            f.set(None)

        with self.assertRaises(Exception):
            f.validate(None)

        s = StringField('test', model=MockModel())
        data = s.validate('test')
        self.assertEqual(data, 'test')

        with self.assertRaises(Exception):
            s.validate(None)

        dt = DateTimeField('test', model=MockModel())
        dt.validate('2018-12-10 15:00:00.123')

        with self.assertRaises(Exception):
            dt.validate('invalid')

        nf = NumberField('test', model=MockModel())
        data = nf.validate(10)
        self.assertEqual(data, 10)

        with self.assertRaises(Exception):
            nf.validate('test')

        af = AutoField('test', model=MockModel())
        val = af.set()
        self.assertEqual(val, 1)

        self.assertEqual(af.set(_id='507f1f77bcf86cd799439011'), {})

        adt = AutoDateTimeField('test', model=MockModel(),create_only=True)
        today = datetime.now().today()

        time = adt.set()
        self.assertEqual(today.date(), time.date())

        new_time = adt.set(_id='507f1f77bcf86cd799439011')
        self.assertEqual(new_time, {})

        bf = BooleanField('test', model=MockModel())
        data = bf.validate(True)
        self.assertTrue(data)

        with self.assertRaises(Exception):
            bf.validate('test')

        fk = ForeignKeyField('test', model=MockModel(), to='test')
        with self.assertRaises(Exception):
            fk.validate('507f1f77bcf86cd799439011')

    def test_model(self):
        app = MockApp()
        model = Model('test', app=app)
        self.assertEqual([], model.fieldnames)
        with self.assertRaises(IndexError):
            self.assertEqual([], model.get_field_by_name('test'))

        model.validate({})
        model.find(test='test', test_two=['test'], test_three=False)
        model.to_repr()

        with self.assertRaises(Exception):
            model.create({})

        with self.assertRaises(Exception):
            model.update(_id='507f1f77bcf86cd799439011', data={})

    def test_methods(self):
        from crudcast.methods import Method
        from crudcast.resources import Resource
        import os
        root = os.path.abspath(os.path.join(__file__, os.pardir))
        file = os.path.join(root, 'mocks.py')

        method = Method(file, '/test/<string:arg1>', 'mocks.TestResource')
        _cls = method.get_resource()
        self.assertTrue(issubclass(_cls, Resource))
