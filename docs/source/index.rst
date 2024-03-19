.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rickle
**************************
.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Contents:

   rickle
   examples
   tools

Starting
=====================
``rickle`` is a versatile Python library and command-line tool that offers a wide range of functionalities for working with YAML and JSON data. Here's a brief summary of its key features:

1. **Serialization**: ``rickle`` allows you to easily serialize Python objects to YAML format. This is particularly useful for converting Python data structures into a human-readable and easily shareable format.

2. **Schema Validation**: It provides the capability to validate YAML and JSON data against predefined schemas. This ensures that your data adheres to a specific structure or format, helping to maintain data consistency.

3. **Schema Generation**: You can generate schema definitions from existing YAML (or JSON) files. This is helpful when you want to formalize the structure of your data or for documentation purposes.

4. **Conversion between YAML and JSON**: ``rickle`` offers seamless conversion between YAML and JSON formats. This facilitates data interchange between systems that use different serialization formats.

5. **Simple Web Server**: One unique feature of ``rickle`` is its ability to create a basic web server from a YAML file. This means you can define endpoints, routes, and data sources purely by writing it as a YAML file, making it easy to prototype web services without extensive coding, or to create mock REST APIs.

In summary, ``rickle`` is a powerful utility for working with YAML and JSON data in Python.
It simplifies tasks like serialization, schema validation, schema generation, format conversion,
and even enables quick web server prototyping using YAML configuration files.
This tool is valuable for developers and data engineers working
with structured data in a flexible and efficient manner.


To install:

.. code-block:: bash

   pip install rickled

Create a YAML file, call it "config.yaml":

.. code-block:: yaml

 BASIC:
  text: test
  dictionary:
    one: 1
    two: 2
  number: 2
  list:
    - one
    - two
    - four
    - name: John
      age: 20
  USERNAME:
    type: env
    load: USERNAME
  callable_lambda:
    type: lambda
    load: "lambda: print('hell world!')"
  datenow:
    type: lambda
    import:
      - "from datetime import datetime as dd"
    load: "lambda: print(dd.utcnow().strftime('%Y-%m-%d'))"
  test_function:
    type: function
    name: test_function
    args:
      x: 7
      y: null
      s: hello world
      any:
        - 1
        - hello
    import:
      - "math"
    load: >
      def test(x, y, s, any):
        print(math.e)
        iii = 111
        print(iii)
        print(x,s)
        if y:
          print(type(y))
        else:
          print(y)
        for i in any:
          print(i)

Then import the tools:

.. code-block:: python

   >> from rickled import Rickle

   >> config = Rickle('./config.yaml', deep=True, load_lambda=True)

   >> config.BASIC.dictionary
   {'one' : 1, 'two' : 2}

   >> config.BASIC.callable_lambda()
   hell world!


About
=====================

``rickle`` is quick to use tool mainly meant to easily encapsulate config YAML files in other Zipfian Science tools.

Changes and history
---------------------

See :ref:`changelog-page` for version history.


Version 1.1.1 (2024-03-19):

* Updated documentation and links to pages.

Contributors
---------------------

* Fabian Sperrle
