.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Helper tools
**************************

Functions
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

.. autofunction:: rickled.tools.flatten_dict

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

.. autofunction:: rickled.tools.inflate_dict

INI parsing helpers
-------------------

The INI helpers transform ``ConfigParser`` objects into Python dictionaries or vice versa and use among other the inflate and flatten functions.

.. autofunction:: rickled.tools.parse_ini

.. autofunction:: rickled.tools.unparse_ini


Other
-------------------

.. autofunction:: rickled.tools.toml_null_stripper

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



.. autoclass:: rickled.tools.Converter
   :members:

Schema tools
=====================
.. autoclass:: rickled.tools.Schema
   :members: