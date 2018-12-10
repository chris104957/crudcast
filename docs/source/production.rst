Running Crudcast in production
==============================

We recommend using Docker to run Crudcast in production. Here's a very simple example using docker-compose:

Folder structure
----------------

Create the following three files in the same folder:

.. code-block:: bash

    - docker-compose.yml
    - Dockerfile
    - config.yml

Docker-compose.yml
------------------

.. code-block:: yaml

    # docker-compose.yml
    version: '3'

    services:
      crudcast:
        build: ./

        ports:
          - "5000:5000"

        links:
         - mongodb

      mongodb:
        image: mongo


Dockerfile
----------

.. code-block:: bash

    FROM python:3.6-alpine
    RUN pip install
    COPY config.yml /
    WORKDIR /
    CMD crudcast --host 0.0.0.0

config.yml
----------

.. code-block:: yaml
    models:
      publisher:
        fields:
          name:
          authors:
            type: manytomany
            to: author

      author:
        fields:
          name:

      book:
        fields:
          name:
          author:
            type: foreignkey
            to: author

    mongo_url: mongodb://mongodb:27017/

How to run it
-------------

.. code-block:: bash
    docker-compose build
    docker-compose up -d