# rickle - Smart Python tools for working with YAML

![PyPI - Version](https://img.shields.io/pypi/v/rickled)
[![Downloads](https://static.pepy.tech/badge/rickled)](https://pepy.tech/project/rickled)
[![Downloads](https://static.pepy.tech/badge/rickled/month)](https://pepy.tech/project/rickled)
[![General badge](https://img.shields.io/badge/Coverage-75+-<COLOR>.svg)](https://zipfian.science/docs/rickle/coverage/index.html)

```
██████╗ ██╗ ██████╗██╗  ██╗██╗     ███████╗
██╔══██╗██║██╔════╝██║ ██╔╝██║     ██╔════╝
██████╔╝██║██║     █████╔╝ ██║     █████╗  
██╔══██╗██║██║     ██╔═██╗ ██║     ██╔══╝  
██║  ██║██║╚██████╗██║  ██╗███████╗███████╗
╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                           
by Zipfian Science                               
```
`rickle` is a versatile Python library and command-line tool that offers a wide range of functionalities for working with YAML and JSON data. Here's a brief summary of its key features:

1. **Serialization**: `rickle` allows you to easily serialize Python objects to YAML format. This is particularly useful for converting Python data structures into a human-readable and easily shareable format.

2. **Schema Validation**: It provides the capability to validate YAML and JSON data against predefined schemas. This ensures that your data adheres to a specific structure or format, helping to maintain data consistency.

3. **Schema Generation**: You can generate schema definitions from existing YAML (or JSON) files. This is helpful when you want to formalize the structure of your data or for documentation purposes.

4. **Conversion between YAML and JSON**: `rickle` offers seamless conversion between YAML and JSON formats. This facilitates data interchange between systems that use different serialization formats.

5. **Simple Web Server**: One unique feature of `rickle` is its ability to create a basic web server from a YAML file. This means you can define endpoints, routes, and data sources purely by writing it as a YAML file, making it easy to prototype web services without extensive coding, or to create mock REST APIs.

In summary, `rickle` is a powerful utility for working with YAML and JSON data in Python. 
It simplifies tasks like serialization, schema validation, schema generation, format conversion, 
and even enables quick web server prototyping using YAML configuration files. 
This tool is valuable for developers and data engineers working 
with structured data in a flexible and efficient manner.

# Usage

For usage examples see [examples](https://zipfian.science/docs/rickle/examples.html) page. 
Documentation can be [found here](https://zipfian.science/docs/rickle/index.html). 

## Install

First install the tool (Python version >= 3.7):

```bash script
$ pip install rickled
```

Optionally the twisted web server can be installed alongside for the `serve` functionality.

```bash script
$ pip install rickled[twisted]
```

Furthermore, if SSL support is needed:

```bash script
$ pip install rickled[twisted,pyopenssl]
```

Check if the installation succeeded:

```bash script
$ rickle --help
```

## Schema tools

Two main schema tools exist, the `check` and the `gen` tools.

### Schema `check`

For checking the schema of input files, the `check` tool is used.

```bash script
$ rickle schema check --help
```

```bash script
$ rickle schema check -i test.yaml -c schema.yaml 
```

### Schema `gen`

Schema files can be generated from YAML files with the `gen` tool.

```bash script
$ rickle schema gen --help
```

```bash script
$ rickle schema gen -i test.yaml
```

This will generate a schema file called `test.schema.yaml`.


## Conversion tools

`rickle` can also be used for bulk conversion from YAML to JSON or the other way around.

```bash script
$ rickle conv --help
```

To convert input files (or directories):

```bash script
$ rickle conv -i test.yaml -o test.json
```

For each input file the output file can be defined and the path suffix is used to infer the desired output type.

Alternatively the type can be specified with the `-t` flag.

## Serving via HTTP(s)

A nifty little use of this Python tool is the ability to host a webserver, using a YAML file.
 
```bash script
$ rickle serve --help
```

```bash script
$ rickle serve -f basic_example.yaml
```

This will start listening on http://localhost:8080, for requests using `GET`. 

# Contributing

As this is an open source project, forks and PRs are welcome! 
Please review some of the practices stated in [CONTRIBUTIONS.md](https://github.com/Zipfian-Science/rickled/blob/master/CONTRIBUTING.md).



© [Zipfian Science](https://zipfian.science) 2020 - 2024
