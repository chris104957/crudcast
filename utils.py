import json
from yaml import load
import pymongo


with open('config.yml', 'r') as f:
    config = load(f.read())


def is_jsonable(x):
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


def _(key, default=default_config):
    return config.get('options', {}).get(key, default[key])


client = pymongo.MongoClient(_('mongo_url'))
db = client[_('db_name')]


def get_config():
    return config


def get_models():
    models = {}

    for model_name, options in config['models'].items():
        m = {
            'name': model_name,
            'collection': db[model_name],
            'fields': options.get('fields', []),
        }
        models[model_name] = m

    return models