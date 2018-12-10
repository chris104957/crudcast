Running your Crudcast app
=========================

Once you've created your Crudcast `config.yml` file, you can start your app with the following command (from the same
folder as your config file):

.. code-block:: bash

    crudcast

Futher options
--------------

Config file
***********

If your `config.yml` is in a different location, you can point Crudcast at it like this:

.. code-block:: bash

    crudcast --config-file /path/to/custom/config.yml

Host
****

By default, Crudcast sets the host name to `0.0.0.0`. This can be overwritten as follows:

.. code-block:: bash

    crudcast --host 127.0.0.1

Port
****

Similary, the default port (`5000`) can also be modified

.. code-block:: bash

    crudcast --port 9000

Import name
***********

It's also possible to specify Flask's `import_name`_ parameter

.. code-block:: bash

    crudcast --import-name myapplication

.. _import_name: http://flask.pocoo.org/docs/0.12/api/#application-object

Debug mode
**********

By default, Debug mode is set to False. You can enable it like this

.. code-block:: bash

    crudcast --debug


Disable dotenv loading
**********************

By default, Flask looks for environmental variables in the nearest :file:`.env` or :file:`.flaskenv` file. To
disable this behaviour, use the following command

.. code-block:: bash

    crudcast --no-load-dotenv
