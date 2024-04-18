CLI Tools
**************************

The command-line interface (CLI) of ``rickle`` enhances its utility by allowing users to perform tasks directly from the terminal without writing extensive scripts.
With this CLI, you can easily convert YAML files to JSON and vice versa, making it an invaluable tool for developers who often need to interchange these formats to accommodate various technologies and frameworks.
Furthermore, the CLI supports schema validation and generation, enabling quick checks and schema creation from YAML or JSON files.
This functionality is especially useful for ensuring data integrity and for rapid prototyping where adherence to predefined data structures is critical.
Overall, rickle's CLI makes it a breeze to manage and transform structured data with simple command-line commands.

To see help and usage:

.. code-block:: shell

    rickle -h

Which will show the list of available options:

.. code-block:: text

   positional arguments:
      {conv,obj,serve,schema}
      conv                Tool for converting files to or from YAML
      obj                 Tool for accessing/manipulating YAML files
      serve               Tool for serving YAML via http(s)
      schema              Tool for generating and checking schemas of
                          YAML files

   optional arguments:
      -h, --help            show this help message and exit
      --version, -v         show version number

.. note::

   Outputs may differ from the documentation.

The main tools that the ``rickle`` CLI exposes are:

1. conv
2. obj
3. schema
4. serve

All of which are discussed in the following sections.

Conversion tool
========================

The conversion process between YAML and JSON using rickle involves a few straightforward steps that can be executed via its command-line interface or programmatically within a Python script.

To see all the available options:

.. code-block:: shell

    rickle conv -h

Which will show the list of available options:

.. code-block:: text

   -h, --help            show this help message and exit
   -i input [input ...]  input file(s) to convert
   -d dir [dir ...]      directory(s) of input files
   -o output [output ...]
                         output file names
   -t type               default output file type (JSON, YAML)
   -s                    suppress verbose output


Convert YAML to JSON
---------------------

To convert an input file ``config.json``, use the following:

.. code-block:: shell

    rickle conv -i config.json

This will create a file ``config.yaml``.

.. note::

   The default output format is YAML. Use ``-t`` option for other formats.

To specify the output type:

.. code-block:: shell

    rickle conv -i config.yaml -t JSON

This will create a ``config.json`` file.

Glob whole directory
---------------------

If the ``-d`` option is used with a directory name, all YAML and JSON files are converted to the same directory.
The ``-t`` option is needed to specify the format or else ``YAML`` will be the default output format.

.. code-block:: shell

    rickle conv -d ./configs -t YAML

This will glob all files in the directory ``./configs``, including JSON and YAML files, and output them as YAML files with the same names.

Define output filenames
---------------------

Input files can have output filenames explicitly defined:

.. code-block:: shell

    rickle conv -i config.yaml -o ./configs/config_dev.json

This will convert ``config.yaml`` to type ``JSON`` (because the type is inferred from the file extension)
with a new name ``config_dev.json`` in the directory ``./configs``.

Multiple files can be converted at once:

.. code-block:: shell

    rickle conv -i config_dev.yaml config_tst.yaml config_prd.yaml -t JSON

When specifying the output names, the order of output filenames must match the order of input files:

.. code-block:: shell

    rickle conv -i config_dev.yaml config_prd.yaml -o confDev.json confPrd.json

Troubleshooting
---------------------

Most likely any occurring error would be a failure to read the file in the given format. File types are inferred from file extensions.
If no file extensions are present, files are inferred by trying to read them in the different formats.
If all fails, no operation is performed and an error message printed.

Object tools
========================

``rickle obj`` is a versatile command-line tool that enhances the functionality of the rickle library by enabling users to
interact directly with YAML (or other formats like JSON) objects from the command line.
With ``rickle obj``, users can perform a variety of operations such as getting the value of an object's attribute,
setting an attribute, deleting an attribute, or executing functions associated with the object.
This tool is especially useful for quick modifications, testing, or automation tasks where direct manipulation of
objects without the need to write full Python scripts can save time and effort.

To see all the available options:

.. code-block:: shell

    rickle obj -h

Which will show the following list of options:

.. code-block:: text

   positional arguments:
      {get,set,del,type,search,func}
      get                 Tool for getting values from YAML files
      set                 Tool for setting values in YAML files
      del                 Tool for deleting keys in YAML files
      type                Tool for checking type of keys in YAML files
      search              Tool for searching keys in YAML files
      func                Tool for executing function defined in YAML
                          files

   optional arguments:
      -h, --help            show this help message and exit
      -i input              input file to read/modify
      -o output             output file to save modified
      -t type               output type (JSON, YAML)
      -l                    load lambda types

Using this tool requires input of a YAML or JSON file. This is done with the ``-i`` option.

.. code-block:: shell

    rickle obj -i config.yaml <VERB>

Where ``<VERB>`` can be one of the following:

.. hlist::
   :columns: 2

   * get
   * set
   * del
   * type
   * search
   * func

These `verbs` will be elaborated on in the next subsections.

Example input
---------------------

In the next examples, the following YAML file will be used as example input:

.. code-block:: yaml
   :linenos:
   :caption: conf.yaml
   :name: conf-yaml

    root_node:
        level_one:
            pswd: password
            usr: name

Document paths
---------------------

An important first concept to understand about using most of the tools ``rickle`` has to offer is
understanding the document paths. A path is the Unix style file and directory path concept applied to
a YAML (or JSON) document.

In the :ref:`example input <conf-yaml>` file, the path to the ``pswd`` key-value pair would be:

.. code-block:: shell

    /root_node/level_one/pswd

Which would have the value ``password``.

.. note::

   The path must always start the slash ``/`` to be valid.

Get
---------------------

To get a value from a document, the key needs to a path in the document.

For example, getting the value of ``pswd``:

.. code-block:: shell

    rickle obj -i conf.yaml get /root_node/level_one/pswd

This will output the value to the command line:

.. code-block:: shell

    password

Just about any paths value can be printed to the command line:

.. code-block:: shell

    rickle obj -i conf.yaml get /root_node/level_one

This will output:

.. code-block:: shell

    pswd: password
    usr: name

To output the entire document:

.. code-block:: shell

    rickle obj -i conf.yaml get /

Will result in:

.. code-block:: shell

    root_node:
      level_one:
         pswd: password
         usr: name

.. note::

   The default output is always YAML. To change the format, add the ``-t`` option to ``obj``.

Outputting the same in JSON:

.. code-block:: shell

    rickle obj -i conf.yaml -t JSON get /

.. code-block:: shell

    {"root_node": {"level_one": {"usr": "name", "pswd": "password"}}}

.. note::

   If the ``-o`` option in ``obj`` is used to output to a file, the result is not printed to screen.

Set
---------------------

To set a value in a document, the key needs be to a path, along with a value.

.. code-block:: shell

    rickle obj -i conf.yaml set /root_node/level_one/pswd **********

This will set the ``pswd`` value to ``**********`` and print the whole document with new value to the command line.

.. code-block:: shell

    root_node:
      level_one:
         pswd: '*********'
         usr: name

.. note::

   If the ``-o`` option in ``obj`` is used to output to a file, the result is not printed to screen.

For example, the following will output to a file:

.. code-block:: shell

    rickle obj -i conf.yaml -t JSON -o conf.json set /root_node/level_one/pswd *********

.. code-block:: json
   :linenos:
   :caption: conf.json
   :name: conf-json

    {"root_node": {"level_one": {"usr": "name", "pswd": "*********"}}}

A new key-value can be added, for example:

.. code-block:: shell

    rickle obj -i conf.yaml set /root_node/level_one/email not@home.com

Results in the added key:

.. code-block:: shell

    root_node:
      level_one:
         pswd: password
         usr: name
         email: not@home.com

This will, however, not work in the following example and result in an error:

.. code-block:: shell

    rickle obj -i conf.yaml set /root_node/level_one/unknown/email not@home.com


Which results in the error message:

.. code-block:: shell

   error: The path /root_node/level_one/unknown/email could not be traversed

Del
---------------------

To remove a value, use the ``del`` option:

.. code-block:: shell

    rickle obj -i conf.yaml del /root_node/level_one/pswd

Resulting in:

.. code-block:: text

   root_node:
      level_one:
         usr: name

Type
---------------------

The ``type`` option will print the Python value type, for example:

.. code-block:: shell

    rickle obj -i conf.yaml type /root_node/level_one/pswd

.. code-block:: text

   <class 'str'>

Or:

.. code-block:: shell

    rickle obj -i conf.yaml type /root_node/level_one

.. code-block:: text

   <class 'rickled.Rickle'>

Search
---------------------

Searching is a useful way to find the paths in a document. The following file with multiple repeated names is used in the examples:

.. code-block:: yaml
   :linenos:
   :caption: conf-multi.yaml
   :name: conf-multi-yaml

    root_node:
        level_one:
            pswd: password
            usr: name
        other:
            usr: joe
        usr: admin


To get the path to ``pswd``:

.. code-block:: shell

    rickle obj -i conf-multi.yaml search pswd

Which will print the path:

.. code-block:: text

   /root_node/level_one/pswd

Where searching for the ``usr`` key:

.. code-block:: shell

    rickle obj -i conf-multi.yaml search usr

...prints the following paths:

.. code-block:: text

   /root_node/usr
   /root_node/level_one/usr
   /root_node/other/usr

Func
---------------------

.. warning::

   Loading unknown code can be potentially dangerous. Only load files that you are fully aware what the Python code will do once executed.
   In general, a safe rule of thumb should be: don't load any Python code.

For using functions, see :ref:`functions <sect-ext-usage-functions>` usage.

.. code-block:: text

   positional arguments:
     key         Key (name) of function
     params      Params for function

   optional arguments:
     -h, --help  show this help message and exit
     -x          infer parameter types

Where ``key`` is the path to the function

For the following example a function ``get_area`` is defined:

.. code-block:: yaml
   :linenos:
   :caption: get-area.yaml
   :name: get-area-yaml

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

To run the function and get the resulting:

.. code-block:: shell

    rickle obj -i get-area.yaml -l func /get_area z:int=10

.. note::

   To load the function the ``-l`` flag must be specified. Please see the warning above again before proceeding.
   Running unknown code is dangerous and should not be done without fully understanding what the code does.

Which will output:

.. code-block:: shell

    420

.. note::

   Parameter types need to be explicitly defined as in the above example ``z:int=10``.
   If no type is defined, all parameters values are assumed to be strings.

The parameter types are:

.. hlist::
   :columns: 2

   * int
   * str
   * float
   * bool
   * list
   * dict

Optionally types can be inferred using the ``-x`` option:

.. code-block:: shell

    rickle obj -i get-area.yaml -l func -x /get_area z=10

Which should infer that ``z`` is an integer.

Consider the following example to work with lists and dictionaries:

.. code-block:: yaml
   :linenos:
   :caption: list-and-dict.yaml
   :name: list-and-dict-yaml

    list_and_dict:
     type: function
     name: list_and_dict
     args:
       list_of_string: null
       dict_type: null
     import:
       - json
     load: >
       def list_and_dict(list_of_string, dict_type):
         if list_of_string:
           for s in list_of_string:
             print(f"{s} - of length {len(s)}")
         if dict_type:
           print(json.dumps(dict_type))

When running:

.. code-block:: shell

    rickle obj -i list-and-dict.yaml -l func -x /list_and_dict list_of_string="['shrt','looong']" dict_type="{'fifty' : 50}"

The output would be:

.. code-block:: shell

   shrt - of length 4
   looong - of length 6
   {"fifty": 50}

Without using the ``-x`` option to infer the values and explicitly defining them:

.. code-block:: shell

    rickle obj -i list-and-dict.yaml -l func /list_and_dict list_of_string:list="['shrt','looong']" dict_type:dict="{'fifty' : 50}"

Would produce the same results.

Troubleshooting
---------------------

1. Get

The most likely problem to occur is if the path can not be traversed, i.e. the path is incorrect:

.. code-block:: shell

    rickle obj -i conf.yaml -t JSON get /path_to_nowhere

And this will result in printing nothing (default behaviour).

Schema tools
========================

Schema tools are useful for either generating schema definitions of files or check files against definitions.

Gen
---------------------

For generating a schema from a file, ``gen`` is used. Consider the following example file:

.. code-block:: yaml
   :linenos:
   :caption: my-example.yaml
   :name: my-example-yaml

   root:
     null_type: null
     dict_type:
       key_one: 99
       key_two: 'text'
     a_string_list:
       - lorem
       - ipsum
     a_floats_list:
       - 0.8
       - 0.9
     a_mixed_list:
       - lorem
       - 0.9

Running the ``gen`` tool:

.. code-block:: shell

    rickle schema gen -i my-example.yaml

will create the file ``my-example.schema.yaml`` as the following:

.. code-block:: yaml
   :linenos:
   :caption: my-example.schema.yaml
   :name: my-example-schema-yaml

   schema:
     root:
       schema:
         a_floats_list:
           schema:
           - type: float
           type: list
         a_mixed_list:
           schema:
           - type: any
           type: list
         a_string_list:
           schema:
           - type: str
           type: list
         dict_type:
           schema:
             key_one:
               type: int
             key_two:
               type: str
           type: dict
         null_type:
           type: any
       type: dict
   type: dict

It will print the following to STDOUT:

.. code-block:: shell

   .\my-example.yaml -> .\my-example.schema.yaml

.. note::

   This can be suppressed by using the ``-s`` flag.

Of course the type can also be defined by either using ``-t``:

.. code-block:: shell

    rickle schema gen -i my-example.yaml -t JSON

Or implicitly with extensions in filenames:

.. code-block:: shell

    rickle schema gen -i my-example.yaml -o my-example.schema.json

Which will result in:

.. code-block:: json
   :linenos:
   :caption: my-example.schema.json
   :name: my-example-schema-json

   {
     "type": "dict",
     "schema": {
       "root": {
         "type": "dict",
         "schema": {
           "null_type": {
             "type": "any"
           },
           "dict_type": {
             "type": "dict",
             "schema": {
               "key_one": {
                 "type": "int"
               },
               "key_two": {
                 "type": "str"
               }
             }
           },
           "a_string_list": {
             "type": "list",
             "schema": [
               {
                 "type": "str"
               }
             ]
           },
           "a_floats_list": {
             "type": "list",
             "schema": [
               {
                 "type": "float"
               }
             ]
           },
           "a_mixed_list": {
             "type": "list",
             "schema": [
               {
                 "type": "any"
               }
             ]
           }
         }
       }
     }
   }



Check
---------------------

The check tool is used to validate file(s) against a schema.

Example:

.. code-block:: shell

    rickle schema check -i my-example.yaml -c my-example.schema.json

Will print the following if passed:

.. code-block:: shell

   my-example.yaml -> OK

Or if failed the test:

.. code-block:: shell

   my-example.yaml -> FAIL

Furthermore a message detailing the failure will be printed, for example:

.. code-block:: shell

   Type 'key_one' == 'str',
    Required type 'int' (per schema {'type': 'int'}),
    In {'key_one': '99', 'key_two': 'text'},
    Path /root/dict_type/key_one

Should output be suppressed, adding the ``-s`` can be used.
Furthermore, failed input files can be moved to directory using ``-o``:

.. code-block:: shell

    rickle schema check -i my-example.yaml -c my-example.schema.json -o ./failed -s

Serve tool
========================

txt

Basic usage
---------------------

txt

Troubleshooting
---------------------

txt