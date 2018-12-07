import json
from yaml import load
import pymongo


with open('config.yml', 'r') as f:
    config = load(f.read())


def is_jsonable(x):
    """
    Helper function to check that a variable can be JSON serialized.

    :param x: Variable to check
    :rtype: Boolean
    """
    try:
        json.dumps(x)
        return True
    except:
        return False


default_config = {
    # database
    "mongo_url": "mongodb://localhost:27017/",
    "db_name": "database",

    # routes
    'base_path': 'api',
}


def get_config_option(key, default=default_config):
    """
    Simple helper function for retrieving config options. If option is populated in the YAML file, this option is
    taken. Otherwise, it falls back to the options in the above `default_config`

    :param key: the config option to be retrieved
    :param default: the default config - defaults to the above `default_config` variable
    """
    return config.get('options', {}).get(key, default[key])


client = pymongo.MongoClient(get_config_option('mongo_url'))
db = client[get_config_option('db_name')]


def get_config():
    """
    Returns the parsed config from the yaml file
    """
    return config


def get_models():
    """
    Populates the model list from the yaml config
    """
    models = {}

    for model_name, options in config['models'].items():
        m = {
            'name': model_name,
            'collection': db[model_name],
            'fields': options.get('fields', []),
        }
        models[model_name] = m

    return models
