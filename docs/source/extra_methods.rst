Adding additional methods to your API
-------------------------------------

You can very easily extend your Crudcast project by creating additional API methods from your own code. This is done
by adding a `methods:` section to your config file

.. code-block:: yaml

    methods:
    - path: say-hello/<string:arg1>
      resource: HelloResource
      file: hello.py

The above will look for a class called `HelloResource` in the file `hello.py`, and insert this method into your API
at the provided path

.. note::
    The `file` attribute can be relative, as shown above, but its generally best to provide the absolute path to this
    file, especially if you're using a custom config file location

Writing methods
---------------

Your custom resources must subclass the `crudcast.resources.Resource` class, which itself extends the
`flask_restplus.Resource` object.

.. code-block:: python

    from crudcast.resources import Resource

    class HelloResource(Resource):
        def get(self, arg1):
            return {'hello': arg1}


Request types
-------------

You can also specify multiple method types in the same resource, as follows:

.. code-block:: python

    from crudcast.resources import Resource
    from flask import request

    class HelloResource(Resource):
        def get(self, arg1):
            return {'hello': arg1}

        def post(self, arg1):
            # do something
            return request.json

Additionally, it is also possible to modify data in your MongoDB collections in your own methods, by using the
`Resource` object's `app` property. For example:

.. code-block:: yaml

    book:
        fields:
          name:
          published:
            type: boolean

    methods:
      - path: books/<string:_id>/publish
        resource: MyBooks
        file: books.py

.. code-block:: python

    from crudcast.resources import Resource
    from pymongo.collection import ObjectId

    class MyBooks(Resource):
        def get(self, _id):
            collection = self.app.db['books']
            collection.find_one_and_update({'_id': ObjectId(_id)}, {'$set': {'published': True}})
            return {'updated': True}

Swagger
-------

As with other methods, your own custom methods will be added to the swagger view. You can modify the information
displayed there by adding a `swagger:` property to the config for your method:

.. code-block:: yaml

    methods:
      - path: books/<string:_id>/publish
        resource: MyBooks
        file: books.py
        swagger:
            summary: Mark a book as published


