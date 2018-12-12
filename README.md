# Crudcast

[![Coverage Status](https://coveralls.io/repos/github/chris104957/crudcast/badge.svg?branch=02-unit-tests)](https://coveralls.io/github/chris104957/crudcast?branch=02-unit-tests)
[![Build Status](https://travis-ci.org/chris104957/crudcast.svg?branch=master)](https://travis-ci.org/chris104957/crudcast)
[![Documentation Status](https://readthedocs.org/projects/crudcast/badge/?version=latest)](https://crudcast.readthedocs.io/en/latest/?badge=latest)


Crudcast lets you build a fully functioning and OpenAPI-compliant CRUD API with a few lines of YAML code.

## Installation

Crudcast requires mongodb - install and start as follows:
```
brew install mongodb
brew service start mongodb
```

Install crudcast

```
pip install crudcast
```

Create a config file, `config.yml`, in the same folder

```
models:
  person:
    fields:
      first_name:
        required: true
      last_name:
        required: true
      age:
        type: number

```

Usage
---

CD into the folder containing your `config.yml`, and run this command
```
crudcast
```
Go to `http://localhost:5000/api/docs` to see your documented and fully-functional API

Documentation
---

Please go to http://crudcast.rtfd.io/ for the full docs

Roadmap
---

Crudcast is brand new and only has a small percentage of the intended functionality so far. In future, I am planning to add support for:

- More authentication methods (OAuth, Token auth, etc)
- Advanced permissions
- inserting your own code - either for validation, permissions or creating your own methods

If there is any other functionality you'd like to see added, then please raise an issue
