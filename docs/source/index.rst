.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pickle Rick
**************************
.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Contents:

   pickle_rick

Starting
=====================
Pickle Rick is a lightweight tool for loading and writing very small Python objects to YAML or JSON representations.
This is especially useful for creating YAML config files and serialising them as Python objects.
Works great in interactive Python environments like notebooks.

To install:

.. code-block:: bash

   pip install pickle-rick

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

   >> from pickle_rick import PickleRick

   >> config = PickleRick('./config.yaml', deep=True, load_lambda=True)

   >> config.BASIC.dictionary
   {'one' : 1, 'two' : 2}

   >> config.BASIC.callable_lambda()
   hell world!


About
=====================

Pickle Rick is quick to use tool mainly meant to easily encapsulate config YAML files in other Zipfian Science tools.

Changes and history
---------------------

See :ref:`changelog-page` for version history.

Version 0.1.12 (2021-09-23)

* Fixed major bug, YAML was not loaded!
* Adding preload arguments for load and replace values within YAML files using ``_|PARAM|_``
* Added new API JSON call method, to load and create a Rick from an API response ``add_api_json_call``.
* Added new ability to load other YAML, JSON, or text files from within, using ``add_from_file``.
* Added ``add_base64`` to load base 64 encoded data.
