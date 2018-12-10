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