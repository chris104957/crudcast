Getting started with Crudcast
=============================

Crudcast is a REST API generator that makes it extremely simple to create a fully-functioning RESTful API

Installing Crudcast
-------------------

Crudcast can be installed with `pip`

.. code-block:: bash

    pip install crudcast


Installing MongoDB
------------------

Crudcast requires MongoDB - it can be installed and run as follows

.. code-block:: bash

    brew install mongodb
    brew service run mongodb

Creating an app
---------------

To create an app, simply create a file called `config.yml` and add the following content

..  code-block:: yaml

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

Running your app
----------------

In the same path as your `config.yml`, open a terminal and run the following command

.. code-block:: bash

    crudcast

Your API is now running on port 5000

.. note::
    To see the full set of available arguments for the `crudcast` command, see `here`_

.. _here: crudcast_command.rst


Using your app
--------------

As well as creating a RESTful API, Crudcast also documents it automatically. Once you've started running your app,
you'll be able to see how it works, and test it, using the Swagger view created at this location:

.. code-block:: bash

    http://localhost:5000/api/docs

Adding users and authentication
-------------------------------

Crudcast also provides an out of the box solution for managing users and basic authentication. To turn on the user
module, simply add the line `users:` to your `config.yml` as a root element

.. code-block:: yaml

    models:
        # model definitions go here
        ...

    users: <= this line

Adding this option will create routes for creating, viewing, updating and deleting users. These routes will be
documented in the swagger view. However, keep in mind that in order to user these routes, you need to be
authenticated. You therefore need to create a user using the command line, before you can use them:

.. code-block:: bash

    crudcast --create-user

    Enter a username: chris
    Enter password:
    Confirm password:

You can now use the above user to create other users via the API.

To require users to authenticate in order to access other routes, simply annotate your models as follows:

.. code-block:: yaml

    models:
      thing:
        fields:
          name:

        auth_type: basic

The above will ensure that you must be authenticated using Basic authorization in order to access all `thing` routes

.. note::
    More auth types will be added in future versions of crudcast

Adding custom methods
---------------------

It's also possible to create API methods with your own custom code - methods can be defined as follows:

.. code-block:: yaml

    methods:
    - path: say-hello/<string:arg1>
      resource: HelloResource
      file: hello.py

`hello.py`:

.. code-block:: python

    from crudcast.resources import Resource

    class HelloResource(Resource):
        def get(self, arg1):
            return {'hello': arg1}

The above will create an additional route as `basePath/say-hello/{arg1}` which returns a simple response. For more
help on this function, see `extra_methods`_

