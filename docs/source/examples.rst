Examples
**************************

There are many uses of ``rickle``, and some of the functionality is described here through examples.

Simple Config
========================

The most basic usage of a ``rickle`` is to use it as a config object. Let's create a scenario in which this might be useful.
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


Here we can see that the config YAML file is loaded as a ``rickle``. In the creation of the Flask API, we load details from the ``rickle``.
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

And then the string will be searched and replaced before the YAML is loaded and a ``rickle`` is constructed.

.. code-block:: python

    from rickled import BaseRickle, Rickle

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

We are not limited to only loading configs from one YAML (or JSON) file. Multiple files can be loaded into one ``rickle`` at once.
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

We can now load both into the same ``rickle``:

.. code-block:: python

    from rickled import BaseRickle, Rickle


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

Strings, Repr
---------------------

A ``rickle`` can have a string representation, which will be in YAML format.

.. code-block:: python

   rick = Rickle('test.yaml')

   print(str(rick))
   >> database:
        host: 127.0.0.1
        user: local
        passw: ken-s3nt_me

Str will give the serialised version where repr will give a raw view.

Dict, Items, Values
---------------------

A ``rickle`` can act like a Python dictionary, like the following examples:

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.items()
   >> [(k, v)]

   rick.values()
   >> [v, v]

   rick.keys()
   >> [k, k]

   rick.get('k', default=0.42)
   >> 72

   rick['new'] = 0.99
   rick['new']
   >> 0.99

A ``rickle`` can also be converted to a Python dictionary:

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.dict()
   >> {'k' : 'v'}


To YAML, JSON
---------------------

A ``rickle`` can also be dumped to YAML or JSON.

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.to_yaml_file('other.yaml')
   rick.to_json_file('other.json')
   rick.to_yaml_string()
   rick.to_json_string()

Extended usage
========================

Add environment var
---------------------

Using the Rickle class, instead of the BasicRickle, we can add a lot more extended types. One being the environment variable.

Here we have a file ``db_conf.yaml`` again, but this time we are loading the values from OS env:

.. code-block:: yaml

   database:
      host:
         type: env
         load: DB_HOST
         default: 127.0.0.1
      user:
         type: env
         load: DB_USERNAME
      passw:
         type: env
         load: DB_PASSWORD

Note that we can define a default value. The default is always None, so no exception is raised if the env var does not exist.

Add lambdas
---------------------

Another extension that could potentially be very useful is adding lambdas to a ``rickle``. This is not without security risks.
If lambdas are loaded that you did not author yourself and do not know what they do, they can do anything.

A ``rickle`` can be loaded without lambdas or functions by passing the ``load_lambda`` argument at creation.
But this is not a foolproof safety measure. Even with ``load_lambda=False``, if you load other sources such as API results or other files, they can reference other calls that do execute the lambda functions.

The safest way to load unknown sources is to not load them. However, you can always define the following ENV variable:

``RICKLE_SAFE_LOAD=1``

Again, the best way to load lambdas is to load what you trust.

Example of a lambda:

.. code-block:: yaml

   datenow:
      type: lambda
      import:
         - "from datetime import datetime as dd"
      load: "print(dd.utcnow().strftime('%Y-%m-%d'))"

The lambda can be used by calling ``datenow()``. Lambdas can also have arguments:

.. code-block:: yaml

   datenow:
      type: lambda
      args:
         message: Hello World
      import:
         - "from datetime import datetime as dd"
      load: "print(dd.utcnow().strftime('%Y-%m-%d'), message)"

And can be used as ``datenow(message='Hello friend')``.

Add functions
---------------------

Functions are a further extension to lambdas. They allow self referencing to the ``rickle``, and are multi line blocks.

.. code-block:: yaml

   get_area:
      type: function
      name: get_area
      args:
         x: 10
         y: 10
         z: null
         f: 0.7
      import:
         - math
      load: >
         def get_area(x, y, z, f):
            if not z is None:
               area = (x * y) + (x * z) + (y * z)
               area = 2 * area
            else:
               area = x * y
            return math.floor(area * f)

And then the function can be called as follows.

.. code-block:: python

   rick = Rickle('test.yaml', load_lambda=True)

   rick.get_area(x=52, y=34.9, z=10, f=0.8)

A self reference to the ``rickle`` can also be added.

.. code-block:: yaml

   const:
      f: 0.7
   get_area:
      type: function
      name: get_area
      is_method: true
      args:
         x: 10
         y: 10
         z: null
      import:
         - math
      load: >
         def get_area(self, x, y, z):
            if not z is None:
               area = (x * y) + (x * z) + (y * z)
               area = 2 * area
            else:
               area = x * y
            return math.floor(area * self.const.f)

In this example ``rickle.const.f`` is used in the function.

This will only work if the attribute referred to is found on the same level. The following example won't work.

.. code-block:: yaml

   const:
      f: 0.7
   one_higher:
      get_area:
         type: function
         name: get_area
         is_method: true
         args:
            x: 10
            y: 10
            z: null
         import:
            - math
         load: >
            def get_area(self, x, y, z):
               if not z is None:
                  area = (x * y) + (x * z) + (y * z)
                  area = 2 * area
               else:
                  area = x * y
               return math.floor(area * self.const.f)

.. code-block:: python

   rick = Rickle('test.yaml', load_lambda=True)

   rick.one_higher.get_area(x=52, y=34.9, z=10, f=0.8)

This will result in an AttributeError:

.. code-block:: python

   >> Traceback (most recent call last):
   >>   File "C:\source\Zipfian Science\rickled\tests\unittest\test_advanced.py", line 183, in test_self_reference
   >>     area = r.functions.get_area(x=10, y=10, z=10)
   >>   File "<string>", line 1, in <lambda>
   >>   File "<string>", line 7, in get_area3ee93073e2f441af9f6a9acac3e21635
   >> AttributeError: 'Rickle' object has no attribute 'const'


Add CSV
---------------------

A local CSV file can be loaded as a list of lists, or as a list of Rickles.

If we have a CSV file with the following contents:

.. code-block:: text

   A,B,C,D
   j,1,0.2,o
   h,2,0.9,o
   p,1,1.0,c

Where ``A,B,C,D`` are the columns, the following will load a list of three ``rickle`` objects.

.. code-block:: yaml

   csv:
      type: from_csv
      file_path: './tests/placebos/test.csv'
      load_as_rick: true
      fieldnames: null

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.csv[0].A == 'j'
   >> True

   rick.csv[0].C == 0.2
   >> True

   rick.csv[-1].D == 'c'
   >> True

If ``fieldnames`` is null, the first row in the file is assumed to be the names.

If the file is not loaded as a Rickle, lists of lists are loaded, and this assumes that the first row is not the field names.

.. code-block:: yaml

   csv:
      type: from_csv
      file_path: './tests/placebos/test.csv'
      load_as_rick: false
      fieldnames: null

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.csv[0]
   >> ['A','B','C','D']

   rick.csv[-1]
   >> ['p',1,1.0,'c']

A third way to load the CSV is to load the columns as lists.

.. code-block:: text

   j,1,0.2,o
   h,2,0.9,o
   p,1,1.0,c

.. code-block:: yaml

   csv:
      type: from_csv
      file_path: './tests/placebos/test.csv'
      load_as_rick: false
      fieldnames: [A, B, C, D]

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.csv.A
   >> ['j','h','p']

   rick.csv.C
   >> [0.2,0.9,1.0]

Add from file
---------------------

Other files can also be loaded, either as another ``rickle``, a binary file, or a plain text file.

.. code-block:: yaml

   another_rick:
      type: from_file
      file_path: './tests/placebos/test_config.json'
      load_as_rick: true
      deep: true
      load_lambda: true

This will load the contents of the file as a ``rickle`` object.

.. code-block:: yaml

   another_rick:
      type: from_file
      file_path: './tests/placebos/test.txt'
      load_as_rick: false
      encoding: UTF-16

This will load the contents as plain text.

.. code-block:: yaml

   another_rick:
      type: from_file
      file_path: './tests/placebos/out.bin'
      is_binary: true

This will load the data as binary.

The data in the file can also be loaded on function call, same as with the ``add_api_json_call``. This is done with the ``hot_load: true`` property.

Add from REST API
---------------------

Data can also be loaded from an API, expecting a JSON response.

.. code-block:: yaml

   crypt_exchanges:
      type: api_json
      url: https://cryptingup.com/api/exchanges
      expected_http_status: 200

This will load the JSON response as a dictionary. But the contents can also be loaded as a ``rickle``.
Note, this can be dangerous, therefore a ``load_lambda`` property is defined. However, this response can point to another API call with ``load_lambda`` set as true.
Only load API responses as Rickles when you trust the contents, or set the ENV ``RICKLE_SAFE_LOAD=1``.

.. code-block:: yaml

   crypt_exchanges:
      type: api_json
      url: https://cryptingup.com/api/exchanges
      expected_http_status: 200
      load_as_rick: true
      deep: true
      load_lambda: false

Other properties that can be defined:

.. code-block:: text

   url
   http_verb: 'GET' or 'POST'
   headers: dictionary type
   params: dictionary type
   body: dictionary type
   load_as_rick: bool
   deep: bool
   load_lambda: bool
   expected_http_status: int
   hot_load: bool

The property ``hot_load`` will turn this into a function that, when called, does the request with the params/headers.

.. code-block:: yaml

   crypt_exchanges:
      type: api_json
      url: https://cryptingup.com/api/exchanges
      expected_http_status: 200
      hot_load: true

This example will load the results hot off the press.

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.crypt_exchanges()

Notice how it is called with parentheses because it is now a function (``hot_load=true``).

Add base 64 encoded
---------------------

A base 64 string can be loaded as bytes.

.. code-block:: yaml

   encoded:
      type: base64
      load: dG9vIG1hbnkgc2VjcmV0cw==


Add HTML page
---------------------

Useful when loading up a documentation page.

.. code-block:: yaml

   encoded:
      type: html_page
      url: https://cryptingup.com
      expected_http_status: 200

This will GET the HTML. ``params`` and ``headers`` can also be given, same as with the API call.

As with the API call, a ``hot_load`` property will load the page on call.

Import Python modules
---------------------

Should you need specific Python modules loaded, you can define the following:

.. code-block:: yaml

   r_modules:
      type: module_import
      import:
         - "math"

Define a class
---------------------

Whole new classes can be defined. This will have a type and will be initialised with attributes and functions.

.. code-block:: yaml

   TesterClass:
      name: TesterClass
      type: class_definition
      attributes:
         dictionary:
            a: a
            b: b
         list_type:
            - 1
            - 2
            - 3
            - 4
    some_func:
      type: function
      name: some_func
      is_method: true
      args:
        x: 7
        y: 2
      import:
        - "math"
      load: >
        def some_func(self, x, y):
          print(x , y)
          print(self.__class__.__name__)
   datenow:
      type: lambda
      import:
        - "from datetime import datetime as dd"
      load: "lambda self: print(dd.utcnow().strftime('%Y-%m-%d'))"

.. code-block:: python

   rick = Rickle('test.yaml')

   rick.TesterClass.datenow()
   >> '1991-02-20'

   print(type(rick.TesterClass))
   >> '<class "TesterClass">'

Paths and searching
========================

Another useful piece of functionality is the ability to use paths with Rickles.

Search keys
---------------------

We can search for paths by using the ``search_path`` method.

.. code-block:: python

   rickle.search_path('point')
   >> ['/config/default/point', '/config/control/point', '/docs/controls/point']

If we search for point, we found all the paths in the ``rickle``.

Use paths
---------------------

We can access the attributes by using the paths. If we have the following YAML:

.. code-block:: yaml

   path:
      datenow:
         type: lambda
         import:
            - "from datetime import datetime as dd"
         load: "dd.utcnow().strftime('%Y-%m-%d')"
      level_one:
         level_two:
            member: 42
            list_member:
               - 1
               - 0
               - 1
               - 1
               - 1
      funcs:
         type: function
         name: funcs
         args:
            x: 42
            y: worl
         load: >
             def funcs(x, y):
                 _x = int(x)
                 return f'Hello {y}, {_x / len(y)}!'

And the we can use paths.

.. code-block:: python

   test_rickle = Rickle(yaml, load_lambda=True)

   test_rickle('/path/level_one/level_two/member') == 42
   >> True

   test_rickle('/path/level_one/funcs?x=100&y=world') == 'Hello world, 20.0!'
   >> True

   test_rickle('/path/datenow')
   >> '1991-08-06'

We can even call functions like this, and pass the arguments as parameters.

Object Rickler
========================

The ObjectRickler is a tool to convert basic Python objects to Rickles, or to create Python objects and merge Rickles into them.
This is very experimental should be used as such.

Object to Rickle
---------------------

A Python object can be converted to a ``rickle``, taking the attributes visible and functions with as best it can.

.. code-block:: python

   class TestObject:

      names = ['Phiber Optik', 'Dark Avenger']
      deep = [
         {'k' : 0.2},
         {'k' : 0.9}
      ]
      __hidden = 'Value'

      def print_names(self):
         for name in self.names:
            print(f'Hello, {name}')

And then using the Rickler:

.. code-block:: python

   rickler = ObjectRickler()

   test_object = TestObject()

   rick = rickler.to_rickle(test_object, deep=True, load_lambda=True)

   isinstance(rick, Rickle)
   >> True

   rick.names
   >> ['Phiber Optik', 'Dark Avenger']

   rick.deep[0].k
   >> 0.2

   rick.print_names()
   >> Hello Phiber Optik
      Hello Dark Avenger

Note that ``__hidden`` will not be a part of the ``rickle``.

The Python object can also be converted to a dictionary.

.. code-block:: python

   obj_dict = rickler.deconstruct(test_object, include_imports=True, include_class_source=True)

   obj_dict['names']
   >> ['Phiber Optik', 'Dark Avenger']

   obj_dict['print_names']
   >> {
          "type": "function",
          "name": "print_names",
          "is_method" : True,
          "load": "def print_names(self):\n         for name in self.names:\n            print(f'Hello, {name}')",
          "args": {}
      }

Rickle to object
---------------------

A ``rickle`` can also be attached to a Python object.

.. code-block:: python

   class TestObject:

      names = ['Phiber Optik', 'Dark Avenger']
      deep = [
         {'k' : 0.2},
         {'k' : 0.9}
      ]
      __hidden = 'Value'

      def print_names(self):
         for name in self.names:
            print(f'Hello, {name}')

And then the following ``rickle`` can be defined:

.. code-block:: yaml

   path:
      datenow:
         type: lambda
         import:
            - "from datetime import datetime as dd"
         load: "dd.utcnow().strftime('%Y-%m-%d')"
      level_one:
         level_two:
            member: 42
            list_member:
               - 1
               - 0
               - 1
               - 1
               - 1
      funcs:
         type: function
         name: funcs
         args:
            x: 42
            y: worl
         load: >
             def funcs(x, y):
                 _x = int(x)
                 return f'Hello {y}, {_x / len(y)}!'

Then added to the object:

.. code-block:: python

   rick = Rickle('test.yaml', load_lambda=True)

   rickler = ObjectRickler()

   obj = rickler.from_rickle(rick, TestObject)

   obj.names
   >> ['Phiber Optik', 'Dark Avenger']

   obj.path.datenow()
   >> '1988-11-02'


