.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

API Reference
**************************

Rickle
========================

BaseRickle
------------------------

The BaseRickle forms the basis for extended versions.
This basis includes important methods for manipulating data, and formulating the internal representation.

.. hlist::
   :columns: 3

   * dict()
   * items()
   * get()
   * set()
   * remove()
   * values()
   * keys()
   * has()
   * search_path()

.. autoclass:: rickle.__init__.BaseRickle
   :members:

Rickle
------------------------

The extended version of BaseRickle that allows for easy loading of external data such as OS environmental variables, files, JSON responses from APIs.
Contains all the same methods in BasicRick such as ``search_path`` etc.

.. autoclass:: rickle.__init__.Rickle
   :members:

UnsafeRickle
------------------------

.. autoclass:: rickle.__init__.UnsafeRickle
   :members:

Object Rickler
========================

The ObjectRickler contains static methods for converting Python objects to Rickle objects for YAML/JSON export,
and then reconstructing the YAML/JSON files to the Python objects. These are not guaranteed to work for all Python objects.

.. autoclass:: rickle.__init__.ObjectRickler
   :members:


Helper tools - Functions
=====================

Flatten dictionaries
---------------------

The ``flatten_dict`` function takes a Python dictionary and makes a thin (shallow) dictionary suitable for lower dimension structures like INI.

.. code-block:: python

   input_dict = {
      'settings': {
         'credentials': {
            'password': 'ken sent me',
            'user': 'larry'
         },
         'nodes': [
            'us-west',
            'us-central',
            'us-east',
         ]
      }
   }

When using the flatten function:

.. code-block:: python

   flatten_dict(input_dict, path_sep='.', list_brackets=('(', ')'))

This will result in the following dictionary:

.. code-block:: python

   {'settings.credentials.password': 'ken sent me',
    'settings.credentials.user': 'larry',
    'settings.nodes.(0)': 'us-west',
    'settings.nodes.(1)': 'us-central',
    'settings.nodes.(2)': 'us-east'}

.. autofunction:: rickle.tools.flatten_dict

Inflate dictionaries
---------------------

Flattened dictionaries in turn can be undone using the ``inflate_dict`` function.
This will recursively built deeper structures as encoded in the keys.

.. code-block:: python
   :linenos:

   flat_dict = {
      'settings.credentials.password': 'ken sent me',
      'settings.credentials.user': 'larry',
      'settings.nodes.(0).name': 'US West',
      'settings.nodes.(0).key': 'us-west',
      'settings.nodes.(1).name': 'US Central',
      'settings.nodes.(1).key': 'us-central',
      'settings.nodes.(2).name': 'US East',
      'settings.nodes.(2).key': 'us-east'
    }

When using the inflate function:

.. code-block:: python

   flatten_dict(input_dict, path_sep='.', list_brackets=('(', ')'))

Will result in the following dictionary:

.. code-block:: python

   {
      'settings': {
         'credentials': {
            'password': 'ken sent me', 'user': 'larry'
          },
          'nodes': [
            {'name': 'US West', 'key': 'us-west'},
            {'name': 'US Central', 'key': 'us-central'},
            {'name': 'US East', 'key': 'us-east'}
          ]
      }
   }

.. autofunction:: rickle.tools.inflate_dict

INI parsing helpers
-------------------

The INI helpers transform ``ConfigParser`` objects into Python dictionaries or vice versa and use among other the inflate and flatten functions.

.. autofunction:: rickle.tools.parse_ini

.. autofunction:: rickle.tools.unparse_ini


Other
-------------------

.. autofunction:: rickle.tools.toml_null_stripper

.. autofunction:: rickle.tools.classify_string

.. autofunction:: rickle.tools.supported_encodings

.. autofunction:: rickle.tools.get_native_type_name

.. autofunction:: rickle.tools.generate_random_value

.. autoclass:: rickle.tools.CLIError

Converter
=====================

The converter is a tool to essentially load a file into a Python dictionary and then dump that dictionary into the target format.
Consider the following YAML file for conversion:

.. code-block:: yaml
   :linenos:
   :name: conf-yaml

   settings:
      credentials:
         password: ken sent me
         user: larry
      nodes:
         - us-west
         - us-central
         - us-east


When using the ``convert_string`` method, the input YAML string can be converted to, for example, XML.

.. code-block:: python

   Converter.convert_string(input_string=input, input_type='yaml', output_type='xml')

.. code-block:: xml
   :linenos:
   :name: conf-xml

   <?xml version="1.0" encoding="utf-8"?>
   <settings>
           <credentials>
                   <password>ken sent me</password>
                   <user>larry</user>
           </credentials>
           <nodes>us-west</nodes>
           <nodes>us-central</nodes>
           <nodes>us-east</nodes>
   </settings>



.. autoclass:: rickle.tools.Converter
   :members:

Schema tools
=====================
.. autoclass:: rickle.tools.Schema
   :members: