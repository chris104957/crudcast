# crudcast

Crudcast lets you build a fully functioning RESTful CRUD API with a few lines of YAML code. It lets you create a fully-functional web app backend for prototyping purposes

## Configuration

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

## Usage

Start the app
```
python views.py
```

Create a new person object
```python
import requests
import json

url = "http://localhost:5000/api/person/"

payload = {
  "first_name": "Chris",
  "last_name": "Davies"
}
headers = {
  'Content-Type': "application/json",
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)

{"_id":"5c06c4137ba4a105ff0427cf","first_name":"Chris","last_name":"Davies"}

```

