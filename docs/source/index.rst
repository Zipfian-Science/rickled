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
`rickle` is a versatile Python library and command-line tool that offers a wide range of functionalities for working with YAML and JSON (and TOML, INI, XML, .ENV) data

1. **Serialization**: `rickle` allows you to easily serialize Python objects to text formats like YAML or JSON.
This is particularly useful for converting Python data structures into a human-readable and easily shareable format, such as `config` files.

2. **Schema Validation**: It provides the capability to validate YAML (and JSON, etc.) data against predefined schemas. This ensures that your data adheres to a specific structure or format, helping to maintain data consistency.

3. **Schema Generation**: Start with easy schema definition generations from existing config files. This is helpful when you want to formalize the structure of your data or for documentation purposes.

4. **Conversion**: `rickle` offers seamless conversion between YAML, JSON, INI, XML, and .ENV formats. This facilitates data interchange between systems that use different serialization formats.

5. **Simple Web Server**: An experimental unique feature of `rickle` is its ability to create a basic web server from a YAML (or JSON, TOML, XML, INI) file. This means you can define endpoints, routes, and data sources purely by writing it as a YAML/etc. file, making it easy to prototype web services without extensive coding, or to create mock REST APIs, or even to serve configuration files as REST APIs.

`rickle` is a powerful utility for working with configuration data in Python.
It simplifies tasks like serialization, schema validation, schema generation, format conversion,
and even enables quick web server prototyping.
This tool is valuable for developers and data engineers working
with structured data in a flexible and efficient manner.


Install
---------------------

.. code-block:: bash

   pip install rickle

Optional extras that can be installed to expand include:

.. code-block:: bash

   pip install rickle[net,xml,dotenv,validators,jsonschema]

Alternatively to install all extras:

.. code-block:: bash

   pip install rickle[full]

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

   >> from rickle import Rickle

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


Version 1.2.2 (2025-02-17):

* Rename of entire project from ``rickled`` to ``rickle``!
* Fixed bug in CLI tool not able to run
* Made ``provider_access_key`` optional for ``secret`` type.

Contributors
---------------------

* Fabian Sperrle

Coverage
---------------------
For a report on the testing coverage, see `coverage report <https://zipfian.science/docs/rickle/coverage/index.html>`_