Field types
===========

This page documents all the different field types available in Crudcast


Manual fields
-------------

Manual fields refers to any model field that can be updated using the REST API.

.. note:: the `required` and `unique` options

    All manual fields support the `required` and `unique` options. `required` fields are fields
    that cannot be null or blank. `unique` fields are fields which must have a unique value for
    the parent model. Note that if a field is `unique`, but not required, the uniqueness validation
    is not performed on null/blank inputs

String fields
*************

String fields are the simplest field type, and accept string inputs only

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_string_field:
                type: string

.. note::
    The **String field** is the default field type. If you do not specify the `type` option,
    the field will be treated as a string field. Adding the `type: string` parameter, as shown
    above, is not necessary

String fields do not support any additional options beyond the `required` or `unique` properties

DateTime fields
***************

Date time fields are used to store date and time information against a model

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_date_time_field:
                type: datetime

By default, DateTime fields accept date time strings in the format `2018-12-29 09:55:00.123`.
You may change the default format using the `format_string` option:

.. code-block:: yaml

    my_date_time_field:
        type: datetime
        format_string: '%d/%m/%y %H:%M'

The above `format_string` would accept the input `21/11/06 16:30`. The `format_string` parameter
accepts any valid formatting string supported by Python's `datetime` library - see `here`_ to see
how to build a valid value for this option

.. _here: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

Number fields
*************

Number fields are just like string fields, but they only accept numeric input

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_number_field:
                type: number

.. note::
    Number fields can accept both integers, e.g. `1`, `2`, `3` or decimal/float values, e,g.
    `1.23`, `3.45`

Number fields do not support any additional options beyond the `required` or `unique` properties

Boolean fields
**************

Boolean fields can store a `true` or `false` input

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_number_field:
                type: boolean

.. warning::
    Although it will theoretically support it, its generally a bad idea to use the `unique`
    parameter on boolean fields

Boolean fields do not support any additional options beyond the `required` or `unique` properties

Foreign key fields
******************

Foreign key fields can be used to store relationships between objects of different types

Usage:

.. code-block:: yaml

    models:
        my_model_one:
            name:

        my_model_two:
            foreignkey_field:
                type: foreignkey
                to: my_model_one

When specifying this field type, you must provide the `to` parameter, which must be the name
of another defined model in the same config file

Foreign key fields are just like text fields, but they store the validated `_id` of another object.

Many to Many fields
-------------------

Many to many fields are like Foreign key fields, but for multiple objects. You can associate an
object with multiple others by using a many to many field

.. code-block:: yaml

    models:
        my_model_one:
            name:

        my_model_two:
            many_to_many_field:
                type: manytomany
                to: my_model_one

As with Foreign key fields, the `to` field must be supplied, and the IDs are validated when the object
is saved. The main difference is that the many to many field stores an array of validated IDs

Auto fields
-----------

As well as manual fields, Crudcast also supports a number of auto fields - fields that are
automatically populated when an object is saved. This type of field does not accept end
user input

_id field
*********

Crudcast uses MongoDB, which allocates a unique Object ID to every document stored in the database.
This ID is set automatically when the document is created, and is used to reference documents in
subsequent lookups. It is automatically addedd to all models and cannot be remove

Auto fields
***********

Auto fields attach an incremental number to each object in your collection

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_auto_field:
                type: autofield

Sending a GET request to the above model would return a response that looked something like this:

.. code-block:: json

    [{
        "id": "",
        "my_auto_field": 1
    }, {
        "id": "",
        "my_auto_field": 2
    }, {
        "id": "",
        "my_auto_field": 3
    }]

Auto fields do not support any additional options

Auto date time field
********************

This field stores a date/time automatically - the value is set when the object is saved

Usage:

.. code-block:: yaml

    models:
        my_model:
            my_auto_date_time_field:
                type: auto_datetime

The auto date time field also supports the `create_only` option, which is set to `False` by
default. If this is set to `True`, then the value is only set when the object is created -
Any further updates to the object would not change the value. Let's look at this example:

.. code-block:: yaml

    models:
        my_model:
            name:
            date_created:
                type: auto_datetime
                create_only: true
            date_changed:
                type: auto_datetime

In the case of the above example, when you create a new instance of the `my_model` object,
the `date_created` and `date_changed` dates would be set to the current date and time. However,
on saving the same instance at a later date, the `date_changed` field would be updated, but
the `date_created` field would remain unchanged



