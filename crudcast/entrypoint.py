from crudcast.api import get_api
import argparse
from crudcast.app import CrudcastApp
from crudcast.exceptions import ValidationError, handle_invalid_usage
import json
import getpass


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    cf = parser.add_argument('--config-file', help='Path to yml config file', dest='config_file', default='config.yml')
    parser.add_argument('--create-user', dest='create_admin', default=False, action='store_true')
    parser.add_argument('--host', help='Host name', dest='host', default='0.0.0.0')
    parser.add_argument('--port', help='Port number', dest='port', default=5000)
    parser.add_argument('--no-load-dotenv', help='Disable dotenv', dest='no_load_dotenv', default=False,
                        action='store_true')
    parser.add_argument('--debug', help='Debug mode', dest='debug', default=False, type=bool)
    parser.add_argument('--import-name', help='Flask app import name', dest='import_name', default='Crudcast')

    args = parser.parse_args()
    create_admin = args.create_admin

    config_file = args.config_file
    import_name = args.import_name
    port = args.port

    debug = args.debug
    host = args.host

    try:
        app = CrudcastApp(import_name=import_name, config_file=config_file)
    except FileNotFoundError:
        raise argparse.ArgumentError(cf, 'Config file not found: %s' % config_file)

    if create_admin:
        user_manager = app.user_manager
        username = input('Enter username: ')
        password = getpass.getpass('Enter password: ')
        password_confirm = getpass.getpass('Confirm password: ')
        try:
            assert password == password_confirm
        except AssertionError:
            raise AssertionError('Passwords do not match')

        user_manager.create({'username': username, 'password': password})
        return 'Created user %s' % username

    else:
        load_dotenv = not args.no_load_dotenv

        get_api(app)
        app.register_error_handler(ValidationError, handle_invalid_usage)

        app.register_blueprint(app.get_swagger_ui_view(), url_prefix=SWAGGER_URL)

        @app.route('/swagger')
        def swagger_file():
            return json.dumps(app.swagger_config)

        app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv)

