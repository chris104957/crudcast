from flask import request
from flask_restplus import Resource as BaseResource
from crudcast.models import Model
from crudcast.users import User


class Resource(BaseResource):
    """
    Extension to the default `flask_restplus.BaseResource` which sets the `app` paramter, which is used for
    model creation
    """
    app = None
    model = None

    def check_auth(self):
        auth_type = self.model.get_auth_type()
        if auth_type:
            return auth_type.authenticate(request=request, user=self.app.user_manager)

    @classmethod
    def set_app(cls, app):
        """
        Sets the value of __class__.app

        :type app: crudcast.app.CrudcastApp
        """
        cls.app = app


class ModelResource(Resource):
    """
    Model level resources - implements all REST methods for paths with no ID
    """
    def get(self, model_name):
        """
        Lists all instances of a given model

        :param model_name: the name of the model, as it appears in the config file
        :return: a list of instances of the model object
        """
        self.model = Model(model_name, self.app)
        user = self.check_auth()
        return self.model.to_repr(**request.args)

    def post(self, model_name):
        """
        Create an instance of a model

        :param model_name: the name of the model, as it appears in the config file
        :return: details of the created instance
        """
        self.model = Model(model_name, self.app)
        user = self.check_auth()
        response = self.model.create(request.json)
        return response


class InstanceResource(Resource):
    """
    Instance level resources - implements all REST methods for paths with an ID
    """
    def get(self, model_name, _id):
        """
        Retrieve a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        :return: the MongoDB document
        """
        self.model = Model(model_name, self.app)
        user = self.check_auth()
        instance = self.model.retrieve(_id)
        return instance

    def put(self, model_name, _id):
        """
        Update a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        :return: the MongoDB document
        """

        self.model = Model(model_name, self.app)
        user = self.check_auth()
        instance = self.model.update(_id=_id, data=request.json)
        return instance

    def delete(self, model_name, _id):
        """
        Delete a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        """

        self.model = Model(model_name, self.app)
        user = self.check_auth()
        instance = self.model.delete(_id=_id)
        return instance


class UserModelResource(Resource):
    def get(self):
        """
        Lists all users

        :return: a list of instances of the user object
        """
        self.model = User(self.app)
        user = self.check_auth()
        return self.model.to_repr(**request.args)

    def post(self):
        """
        Create a user

        :return: details of the created user
        """
        self.model = User(self.app)
        user = self.check_auth()
        return self.model.create(request.json)


class UserInstanceResource(Resource):
    """
    Instance level resources - implements all REST methods for paths with an ID
    """
    def get(self, _id):
        """
        Retrieve a single instance by its ID

        :param _id: MongoDB _id string
        :return: the MongoDB document
        """
        self.model = User(self.app)
        print('manager', self.app.user_manager)
        user = self.check_auth()
        return self.model.retrieve(_id)

    def put(self, _id):
        """
        Update a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        :return: the MongoDB document
        """

        self.model = User(self.app)
        user = self.check_auth()
        return self.model.update(_id=_id, data=request.json)

    def delete(self, _id):
        """
        Delete a single instance by its ID

        :param _id: MongoDB _id string
        """

        self.model = User(self.app)
        user = self.check_auth()
        return self.model.delete(_id=_id)
