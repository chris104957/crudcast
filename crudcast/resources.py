from flask import request
from flask_restplus import Resource as BaseResource
from .models import Model


class Resource(BaseResource):
    """
    Extension to the default `flask_restplus.BaseResource` which sets the `app` paramter, which is used for
    model creation
    """
    app = None

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
        model = Model(model_name, self.app)
        return model.to_repr(**request.args)

    def post(self, model_name):
        """
        Create an instance of a model

        :param model_name: the name of the model, as it appears in the config file
        :return: details of the created instance
        """
        model = Model(model_name, self.app)
        response = model.create(request.json)
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
        model = Model(model_name, self.app)
        instance = model.retrieve(_id)
        return instance

    def put(self, model_name, _id):
        """
        Update a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        :return: the MongoDB document
        """

        model = Model(model_name, self.app)
        instance = model.update(_id=_id, data=request.json)
        return instance

    def delete(self, model_name, _id):
        """
        Delete a single instance by its ID

        :param model_name: the name of the model, as it appears in the config file
        :param _id: MongoDB _id string
        """

        model = Model(model_name, self.app)
        instance = model.delete(_id=_id)
        return instance



