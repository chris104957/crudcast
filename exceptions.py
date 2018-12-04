class ValidationError(Exception):
    status_code = 400

    def __init__(self, message, field=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.field = field

    def to_dict(self):
        return {self.field: self.message}
