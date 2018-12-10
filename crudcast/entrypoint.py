from .api import get_api
import argparse
from .app import CrudcastApp
from .exceptions import ValidationError, handle_invalid_usage
import json

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    cf = parser.add_argument('--config-file', help='Path to yml config file', dest='config_file', default='config.yml')
    parser.add_argument('--host', help='Host name', dest='host', default='0.0.0.0')
    parser.add_argument('--port', help='Port number', dest='port', default=5000)
    parser.add_argument('--no-load-dotenv', help='Disable dotenv', dest='no_load_dotenv', default=False, type=bool)
    parser.add_argument('--debug', help='Debug mode', dest='debug', default=False, type=bool)
    parser.add_argument('--import-name', help='Flask app import name', dest='import_name', default='Crudcast')

    args = parser.parse_args()
    config_file = args.config_file
    import_name = args.import_name
    port = args.port

    debug = args.debug
    host = args.host

    try:
        app = CrudcastApp(import_name=import_name, config_file=config_file)
    except FileNotFoundError:
        raise argparse.ArgumentError(cf, 'Config file not found: %s' % config_file)

    load_dotenv = not args.no_load_dotenv

    get_api(app)
    app.register_error_handler(ValidationError, handle_invalid_usage)

    app.register_blueprint(app.get_swagger_ui_view(), url_prefix=SWAGGER_URL)

    @app.route('/swagger')
    def swagger_file():
        return json.dumps(app.swagger_config)

    app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv)
