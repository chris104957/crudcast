from flask import request
from flask_restplus import Resource
from .models import Model


class ModelResource(Resource):
    def get(self, model_name):
        model = Model(model_name)
        return model.to_repr(**request.args)

    def post(self, model_name):
        model = Model(model_name)
        response = model.create(request.json)
        return response


class InstanceResource(Resource):
    def get(self, model_name, _id):
        model = Model(model_name)
        instance = model.retrieve(_id)
        return instance

    def put(self, model_name, _id):
        model = Model(model_name)
        instance = model.update(_id=_id, data=request.json)
        return instance

    def delete(self, model_name, _id):
        model = Model(model_name)
        instance = model.delete(_id=_id)
        return instance



