from werkzeug.exceptions import BadRequest
from flask import jsonify


def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


class ValidationError(BadRequest):
    """
    When invalid data is sent to via POST or PUT, this exception gets raised

    :param message: The error message
    :param field: The name of the field that raised the exception, if applicable
    :param status_code: allows overwriting of the default bad request status code, 400
    """
    status_code = 400

    def __init__(self, message, field=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.field = field

    def to_dict(self):
        """
        Returns a REST-friendly API response
        """
        return {self.field: self.message}


class ConfigException(Exception):
    """
    This exception gets raised if the config file is invalid
    """
    pass
