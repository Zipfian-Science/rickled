.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rickle Picking
**************************

Simple classes for encapsulating Python objects, with functions to write these simple objects to YAML or JSON.

Basic Rickle
========================
.. autoclass:: rickled.__init__.BaseRickle
   :members:

Rickle Pick
========================

An extended version of BaseRickle that allows extra easy loading, including Python functions, lambdas, and OS environmental variables.
Contains all the same methods in BasicRick.

.. autoclass:: rickled.__init__.Rickle
   :members:

Object Rickler
========================

The ObjectRickler attempts to convert Python objects to Rickle objects for YAML/JSON export, and then reconstructing the YAML/JSON files to the Python objects.

.. autoclass:: rickled.__init__.ObjectRickler
   :members: