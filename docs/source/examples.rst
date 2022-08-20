.. Natural Selection documentation master file, created by
   sphinx-quickstart on Tue Sep 22 22:57:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Examples
**************************
.. contents:: Table of Contents

There are many uses of Rickle, and some of the functionality is described here through examples.

Simple Config
========================

The most basic usage of a Rickle is to use it as a config object. Let's create a scenario in which this might be useful.
Say you have a common API served through a Flask app. You need 10 versions of the API, each having the same code base but with different databases in the back, and some different endpoint configurations.
Below we follow an example app with 10 different configs saved as YAML files.

Basic usage
---------------------

Let's make our first simple config in YAML, call it ``config_US.yaml``.

.. code-block:: yaml

 APP:
    details:
        name: user_api
        doc_page: '/doc'
        version: '1.0.0'
    database:
        host: 127.0.0.1
        user: local
        passw: ken-s3nt_me
    endpoints:
        status:
            description: Gets the status for a region in the country.
            params:
                region: US
                language: en-US
        users:
            description: Gets the users for a given city.
            params:
                city: Seattle

As an example, we will have the simple API:

.. code-block:: python

    from flask import Flask, Resource
    from flask_restx import Api
    from rickled import BaseRickle
    from some_database import DBConnection

    config = BaseRickle('./config_US.yaml')

    app = Flask(config.APP.details.name)
    api = Api(
        app,
        version=config.APP.details.version,
        doc=config.APP.details.doc_page,
    )

    conf_status_ep = config.APP.endpoints.get('status')
    if conf_status_ep:
        @api.route('/status')
        class Status(Resource):
            @api.doc(description=conf_status_ep.description)
            @api.param('region', conf_status_ep.params.region)
            @api.param('language', conf_status_ep.params.language)
            def get(self):
                return some_function_here(request.args['region'], request.args['language'])

    conf_users_ep = config.APP.endpoints.get('users')
    if conf_users_ep:
        @api.route('/users')
        class Users(Resource):
            @api.doc(description=conf_users_ep.description)
            @api.param('city', conf_users_ep.params.city)
            def get(self):
                with DBConnection(host=config.APP.database.host,
                                  user=config.APP.database.user,
                                  passw=config.APP.database.passw
                                 ) as conn:
                    results = conn.exec(f"SELECT * FROM users WHERE city = '{request.args['city']}'")
                return results


Here we can see that the config YAML file is loaded as a Rickle. In the creation of the Flask API, we load details from the Rickle.
We then get the settings for the endpoint "status". If the endpoint is not defined in the YAML, we simply don't create it.
That gives us the power to create a new YAML config for another country where the "status" endpoint does not exist.


Create from different things
----------------------------

The config does not have to be loaded from a YAML file. It does not even have to be loaded.

.. code-block:: python

    # Create an empty Rickle
    config = BaseRickle()

    # Loaded from a JSON file
    config = BaseRickle('./config_ZA.json')

    # Create from a Python dictionary
    d = {
        'APP' : {
            'details': {
                'name': 'user_api',
                'doc_page': '/doc',
                'version': '1.0.0'
            }
            'database': {
                'host': '127.0.0.1',
                'user': 'local',
                'passw': 'ken-s3nt_me'
           }
            'endpoints': {}
        }
    }
    config = BaseRickle(d)

    # Create from a YAML string (or a JSON string)
    yaml_string = """
    APP:
        details:
            name: user_api
            doc_page: '/doc'
            version: '1.0.0'
        database:
            host: 127.0.0.1
            user: local
            passw: ken-s3nt_me
        endpoints: null
    """

    config = BaseRickle(yaml_string)


Add global arguments
---------------------

For the less likely event that you need to modify the YAML string dynamically before loading, arguments can be given as follows.

.. code-block:: yaml

 APP:
    details:
        name: user_api
        doc_page: _|documentation_endpoint|_
        version: '1.0.0'

And then the string will be searched and replaced before the YAML is loaded and a Rickle is constructed.

.. code-block:: python

    # Create an empty Rickle
    config = BaseRickle()

    # Loaded from a JSON file
    config = BaseRickle('./config_ZA.json', documentation_endpoint='/za_docs')

This will in effect change the YAML to the following (before loading it).

.. code-block:: yaml

 APP:
    details:
        name: user_api
        doc_page: /za_docs
        version: '1.0.0'

Even though the possibilities are opened up here, there are probably better ways to solve this (such as using ENV vars as shown later in this examples page).

Load multiple files
---------------------

We are not limited to only loading configs from one YAML (or JSON) file. Multiple files can be loaded into one Rickle at once.
Be sure to not have duplicate keys in the same root.

Let's create the same config but split it into two, because we probably have the same DB connection details for all 10 countries.

Here we have a file ``db_conf.yaml``:

.. code-block:: yaml

    database:
        host: 127.0.0.1
        user: local
        passw: ken-s3nt_me

And now the country config ``config_SW.yaml``:

.. code-block:: yaml

    details:
        name: user_api
        doc_page: /docs
        version: '1.0.0'

Notice how here we don't have the root ``APP``, but only to show the example.

We can now load both into the same Rickle:

.. code-block:: python

    # Load a list of YAML files
    config = BaseRickle(['./db_conf.yaml', './config_SW.yaml'])

    print(config.database.host)
    print(config.details.version)

Again, in this example the root ``APP`` is missing as it is a slightly different example.

In this example we can create 10 config files and always load the same DB connection settings, instead of copying it to each config file.

Referencing in YAML
---------------------

What is especially powerful of YAML is the ability to add references.
If we had a lot of duplication, we can simply reference the same values.

.. code-block:: yaml

APP:
   details:
       name: user_api
       doc_page: '/doc'
       version: '1.0.0'
   database:
       host: 127.0.0.1
       user: local
       passw: ken-s3nt_me
   default_params:
      db_version: &db_version '1.1.0'
      language: &language 'en-US'
   endpoints:
      status:
         description: Gets the status for a region in the country.
         params:
            region: US
            language: *language
            db_version: *db_version
      users:
         description: Gets the users for a given city.
         params:
            city: Seattle
            language: *language
            db_version: *db_version




Extended usage
========================

Add environment var
---------------------

Add lambdas
---------------------

Add functions
---------------------

Add CSV
---------------------

Add from file
---------------------

Add from REST API
---------------------

Add base 64 bin
---------------------

Paths and searching
========================

Search keys
---------------------

Use paths
---------------------

Object rickler
========================

Object to Rickle
---------------------

Rickle to object
---------------------

