.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Rickle Picking
**************************
.. contents:: Table of Contents

Simple classes for encapsulating Python objects, with functions to write these simple objects to YAML or JSON.

Basic Rickle
========================
.. autoclass:: rickle.__init__.BaseRickle
   :members:

Rickle Pick
========================

An extended version of BasicRick that allows extra easy loading, including Python functions, lambdas, and OS environmental variables.
Contains all the same methods in BasicRick.

.. autoclass:: rickle.__init__.Rickle
   :members: