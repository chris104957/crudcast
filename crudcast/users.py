from crudcast.models import Model
from crudcast.exceptions import ValidationError
from flask import abort
import bcrypt


class User(Model):
    config = {
        'username_field': 'username'
    }  # default user config

    @property
    def username_field(self):
        return self.config['username_field']

    def to_repr(self, **query):
        """
        Remove the hashed password from the response
        """
        output = super(User, self).to_repr(**query)
        new_output = []
        for user in output:
            new_user = {}
            for key, val in user.items():
                if key not in ['password', 'salt']:
                    new_user[key] = val
            new_output.append(new_user)

        return new_output

    def __init__(self, app, **options):
        for key, val in options.items():
            self.config[key] = val

        super().__init__('user', app=app)

    def user_exists(self, username):
        return self.collection.find({self.username_field: username}).count() == 1

    def check_invalid_keys(self, keys):
        key = None
        try:
            for key in keys:
                assert key in [self.username_field, 'password']
        except AssertionError:
            raise ValidationError('Invalid field', field=key)

    def validate(self, data=None, _id=None):
        if not data:
            data = {}

        if not _id:
            try:
                assert self.username_field in data.keys()
                assert 'password' in data.keys()

            except AssertionError:
                raise ValidationError('Username and password must be provided')

            if self.user_exists(data[self.username_field]):
                raise ValidationError('That user already exists')

        return data

    def hash_password(self, raw_password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(raw_password.encode(), salt), salt

    def authenticate(self, username, password):
        if not username or not password:
            abort(401)

        try:
            users = self.find(**{self.username_field: username})
            assert users.count() == 1
            user = users[0]
            self.verify_password(username, password)
            return user

        except AssertionError:
            abort(401)

    def update(self, _id, data):
        """
        Method extended to hash the password, if a new one is provided
        """

        # the below validation is done at this level to prevent manual insertion of salt
        self.check_invalid_keys(data.keys())

        if data.get('password'):
            data['password'], data['salt'] = self.hash_password(data.pop('password'))

        return super().update(_id, data)

    def create(self, data):
        if data.get('password'):
            password = data.pop('password')
            data['password'], data['salt'] = self.hash_password(password)
        return super().create(data)

    def verify_password(self, username, password):
        users = self.find(**{self.username_field: username})
        hash = users[0]['password']
        salt = users[0]['salt']
        valid = bcrypt.hashpw(password.encode(), salt) == hash
        if not valid:
            abort(401)
