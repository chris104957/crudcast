import base64
from flask import abort


class BaseAuthHandler(object):
    @classmethod
    def authenticate(cls, request, user):
        raise NotImplementedError()


class BasicAuth(object):
    @classmethod
    def authenticate(cls, request, user):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            abort(401)

        enc = auth_header.split()[1]
        decoded = base64.b64decode(enc.encode())
        username, password = decoded.decode().split(':')

        return user.authenticate(username, password)



