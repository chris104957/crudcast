from werkzeug.exceptions import BadRequest
from flask import jsonify


def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


class ValidationError(BadRequest):
    status_code = 400

    def __init__(self, message, field=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.field = field

    def to_dict(self):
        return {self.field: self.message}


class ConfigException(Exception):
    pass
