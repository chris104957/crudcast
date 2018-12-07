from .api import get_api
import argparse
from .app import CrudcastApp
from .exceptions import ValidationError, handle_invalid_usage
import json

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    cf = parser.add_argument('--config-file', help='Path to yml config file', dest='config_file', default='config.yml')
    parser.add_argument('--import-name', help='Flask app import name', dest='import_name', default='Crudcast')

    args = parser.parse_args()
    config_file = args.config_file
    import_name = args.import_name

    try:
        app = CrudcastApp(import_name=import_name, config_file=config_file)
    except FileNotFoundError:
        raise argparse.ArgumentError(cf, 'Config file not found: %s' % config_file)

    get_api(app)
    app.register_error_handler(ValidationError, handle_invalid_usage)

    # Register blueprint at URL
    # (URL must match the one given to factory function above)
    app.register_blueprint(app.get_swagger_ui_view(), url_prefix=SWAGGER_URL)

    @app.route('/swagger')
    def swagger_file():
        return json.dumps(app.swagger_config)

    app.run()
