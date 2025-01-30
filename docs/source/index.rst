.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rickle
**************************
.. toctree::
   :maxdepth: 1
   :numbered:
   :caption: Contents:

   api_reference
   examples
   cli_tools
   changelog

About
=====================
``rickle`` is a versatile Python library and command-line tool that offers a wide range of functionalities for working with YAML, JSON, and TOML data data. Here's a brief summary of its key features:

1. **Serialization**: ``rickle`` allows you to easily serialize Python objects to YAML (or other) format. This is particularly useful for converting Python data structures into a human-readable and easily shareable format.

2. **Schema Validation**: It provides the capability to validate YAML and JSON data against predefined schemas. This ensures that your data adheres to a specific structure or format, helping to maintain data consistency.

3. **Schema Generation**: You can generate schema definitions from existing YAML (or JSON) files. This is helpful when you want to formalize the structure of your data or for documentation purposes.

4. **Conversion between formats**: ``rickle`` offers seamless conversion between YAML and JSON formats. This facilitates data interchange between systems that use different serialization formats.

5. **Simple Web Server**: One unique feature of ``rickle`` is its ability to create a basic web server from a YAML file. This means you can define endpoints, routes, and data sources purely by writing it as a YAML file, making it easy to prototype web services without extensive coding, or to create mock REST APIs.

In summary, ``rickle`` is a powerful utility for working with YAML, JSON, and TOML data in Python.
It simplifies tasks like serialization, schema validation, schema generation, format conversion,
and even enables quick web server prototyping using YAML configuration files.
This tool is valuable for developers and data engineers working
with structured data in a flexible and efficient manner.


Install
---------------------

.. code-block:: bash

   pip install rickled

Optional extras that can be installed to expand include:

.. code-block:: bash

   pip install rickled[net,xml,dotenv,validators,jsonschema]

Alternatively to install all extras:

.. code-block:: bash

   pip install rickled[full]

Quick start
---------------------

Create a YAML file, call it "config.yaml":

.. code-block:: yaml
   :linenos:
   :caption: config.yaml
   :name: config-example-yaml

   conf:
      db_connection:
         acc_name:
            type: env
            load: ACC_NAME
            default: developer_account
         acc_pass:
            type: env
            load: ACC_PASS
         database_name: public

Then import the tools:

.. code-block:: python

   >> from rickled import Rickle

   >> config = Rickle('./config.yaml')

   >> config.conf.db_connection.dict()
   {'acc_name' : 'acceptance_account', 'acc_pass' : 'asd!424iXj', 'database_name' : 'public'}

   >> config.conf.db_connection.acc_pass
   'asd!424iXj'

   >> config('/conf/db_connection/acc_pass')
   'asd!424iXj'

For more examples of usage see :ref:`examples-page`. See :ref:`cli-page` for CLI usage.

Changes and history
---------------------

See :ref:`changelog-page` for version history.


Version 1.1.3 (2024-05-05):

* Major addition: TOML now supported

Contributors
---------------------

* Fabian Sperrle

Coverage
---------------------
For a report on the testing coverage, see `coverage report <https://zipfian.science/docs/rickle/coverage/index.html>`_