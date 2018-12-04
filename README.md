# crudcast

Crudcast lets you build a fully functioning RESTful CRUD API with a few lines of YAML code.

## Usage

Clone this repository
```
git clone https://github.com/chris104957/crudcast.git
```

cd into the folder
```
cd crudcast
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
