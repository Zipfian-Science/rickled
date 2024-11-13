# ASCCI Text found in this file was generated on
# https://patorjk.com/software/taag/
# Large heading using "Shaded Blocky" font
# Sub headings using "Small" font
import importlib.util
import os
import sys
import warnings
from enum import Enum
from io import StringIO

import rickled.__version__ as ver
import argparse
from rickled.tools import cli_bcolors, unparse_ini
from rickled.tools import Schema
from rickled.tools import Converter
from rickled.tools import toml_null_stripper

from rickled import Rickle, UnsafeRickle
import re
import json
import yaml
import ast

import tomli_w as tomlw

GITHUB_DOCS_URL = "https://github.com/Zipfian-Science/rickled/blob/master/docs/source/cli_tools.rst#cli-tools"

class CLIError(Exception):

    class CLITool(Enum):
        CONV = 1
        OBJ = 2
        SERVE = 3
        SCHEMA = 4
        OBJ_GET = 5
        OBJ_SET = 6
        OBJ_DEL = 7
        OBJ_TYPE = 8
        OBJ_SEARCH = 9
        OBJ_FUNC = 10
        SCHEMA_CHECK = 11
        SCHEMA_GEN = 12


    def __init__(self, message, cli_tool: CLITool):
        self.message = message
        self.cli_tool = cli_tool

    def __str__(self):
        return f"{self.cli_tool} {self.message}"


def conv(args):
    try:
        if args.INPUT or args.INPUT_DIRECTORY:
            Converter(input_files=args.INPUT,
                      output_files=args.OUTPUT,
                      input_directory=args.INPUT_DIRECTORY,
                      default_output_type=args.OUTPUT_TYPE,
                      verbose=args.VERBOSE).do_convert()
        elif args.OUTPUT_TYPE:
            data = sys.stdin.read()

            converted = Converter.convert_string(input_string=data,
                                                 input_type=args.INPUT_TYPE,
                                                 output_type=args.OUTPUT_TYPE)

            print(converted)
        else:
            raise CLIError(message='Incorrect usage of CLI tool, refer to documentation', cli_tool=CLIError.CLITool.CONV)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.CONV)

def obj_get(args):
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()

            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)

            v = r.get(args.key)
            dump_type = args.OUTPUT_TYPE.lower()

            if isinstance(v, Rickle):
                v = v.dict()
            if isinstance(v, dict):
                v = v
            elif v is None:
                v = ''

            if args.OUTPUT:

                if dump_type == 'yaml':
                    with open(args.OUTPUT, 'w') as fp:
                        yaml.safe_dump(v, fp)
                elif dump_type == 'json':
                    with open(args.OUTPUT, 'w') as fp:
                        json.dump(v, fp)
                elif dump_type == 'toml':
                    with open(args.OUTPUT, 'wb') as fp:
                        tomlw.dump(toml_null_stripper(v), fp)
                elif dump_type == 'xml':
                    if importlib.util.find_spec('xmltodict'):
                        import xmltodict
                        with open(args.OUTPUT, 'wb') as fp:
                            xmltodict.unparse(v, fp)
                    else:
                        raise ImportError("Missing 'xmltodict' dependency")
                elif dump_type == 'ini':
                    if isinstance(v, dict):
                        path_sep = os.getenv("RICKLE_INI_PATH_SEP", ".")
                        list_brackets = (
                            os.getenv("RICKLE_INI_OPENING_BRACES", "("), os.getenv("RICKLE_INI_CLOSING_BRACES", ")")
                        )
                        v = toml_null_stripper(v)
                        output_ini = unparse_ini(dictionary=v, path_sep=path_sep, list_brackets=list_brackets)

                        with open(args.OUTPUT, 'w') as fp:
                            output_ini.write(fp)

                    else:
                        raise CLIError("Can only dump dictionary type to INI", cli_tool=CLIError.CLITool.OBJ_GET)
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_GET)

            else:
                if dump_type == 'yaml':
                    print(yaml.safe_dump(v))
                elif dump_type == 'json':
                    print(json.dumps(v))
                elif dump_type == 'toml':
                    print(tomlw.dumps(toml_null_stripper(v)))
                elif dump_type == 'xml':
                    if importlib.util.find_spec('xmltodict'):
                        import xmltodict

                        print(xmltodict.unparse(v, pretty=True))
                    else:
                        raise ImportError("Missing 'xmltodict' dependency")
                elif dump_type == 'ini':
                    if isinstance(v, dict):
                        path_sep = os.getenv("RICKLE_INI_PATH_SEP", ".")
                        list_brackets = (
                            os.getenv("RICKLE_INI_OPENING_BRACES", "("), os.getenv("RICKLE_INI_CLOSING_BRACES", ")")
                        )
                        v = toml_null_stripper(v)
                        output_ini = unparse_ini(dictionary=v, path_sep=path_sep, list_brackets=list_brackets)

                        out = StringIO()
                        output_ini.write(out)
                        out.seek(0)

                        print(out.read())
                    else:
                        raise CLIError("Can only dump dictionary type to INI", cli_tool=CLIError.CLITool.OBJ_GET)
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_GET)


    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_GET)



def obj_set(args):
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            r.set(args.key, args.value)
            dump_type = args.OUTPUT_TYPE.lower()

            if args.OUTPUT:
                if dump_type == 'yaml':
                    r.to_yaml(output=args.OUTPUT)
                elif dump_type == 'json':
                    r.to_json(output=args.OUTPUT)
                elif dump_type == 'toml':
                    r.to_toml(output=args.OUTPUT)
                elif dump_type == 'xml':
                    r.to_xml(output=args.OUTPUT)
                elif dump_type == 'ini':
                    r.to_ini(output=args.OUTPUT)
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_SET)

            else:
                if dump_type == 'yaml':
                    print(r.to_yaml())
                elif dump_type == 'json':
                    print(r.to_json())
                elif dump_type == 'toml':
                    print(r.to_toml())
                elif dump_type == 'xml':
                    print(r.to_xml())
                elif dump_type == 'ini':
                    print(r.to_ini())
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_SET)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_SET)


def obj_del(args):
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            r.remove(args.key)
            dump_type = args.OUTPUT_TYPE.lower()

            if args.OUTPUT:
                if dump_type == 'yaml':
                    r.to_yaml(output=args.OUTPUT)
                elif dump_type == 'json':
                    r.to_json(output=args.OUTPUT)
                elif dump_type == 'toml':
                    r.to_toml(output=args.OUTPUT)
                elif dump_type == 'xml':
                    r.to_xml(output=args.OUTPUT)
                elif dump_type == 'ini':
                    r.to_ini(output=args.OUTPUT)
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_DEL)
            else:
                if dump_type == 'yaml':
                    print(r.to_yaml())
                elif dump_type == 'json':
                    print(r.to_json())
                elif dump_type == 'toml':
                    print(r.to_toml())
                elif dump_type == 'xml':
                    print(r.to_xml())
                elif dump_type == 'ini':
                    print(r.to_ini())
                else:
                    raise CLIError(f"Unsupported dump type {dump_type}", cli_tool=CLIError.CLITool.OBJ_DEL)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_DEL)

def obj_type(args):
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            v = r.get(args.key)

            yaml_types = {
                'str': 'str',
                'int': 'int',
                'float': 'float',
                'bool': 'boolean',
                'list': 'seq',
                'dict': 'map',
                'Rickle': 'map',
                'UnsafeRickle': 'map',
                'BaseRickle': 'map',
                'bytes': 'binary'
            }

            json_types = {
                'str': 'string',
                'int': 'number',
                'float': 'number',
                'bool': 'boolean',
                'list': 'array',
                'dict': 'object',
                'Rickle': 'object',
                'UnsafeRickle': 'object',
                'BaseRickle': 'object',
            }

            toml_types = {
                'str': 'String',
                'int': 'Integer',
                'float': 'Float',
                'bool': 'Boolean',
                'list': 'Array',
                'dict': 'Key/Value',
                'Rickle': 'Key/Value',
                'UnsafeRickle': 'Key/Value',
                'BaseRickle': 'Key/Value',
            }

            xml_types = {
                'str': 'xs:string',
                'int': 'xs:integer',
                'float': 'xs:decimal',
                'bool': 'xs:boolean',
                'list': 'xs:sequence',
                'dict': 'xs:complexType',
                'Rickle': 'xs:complexType',
                'UnsafeRickle': 'xs:complexType',
                'BaseRickle': 'xs:complexType',
            }

            output_type = args.OUTPUT_TYPE.strip().lower()

            python_type = type(v).__name__

            if output_type == 'yaml':
                print(yaml_types.get(python_type, 'Python'))
            elif output_type == 'json':
                print(json_types.get(python_type, 'object'))
            elif output_type == 'toml':
                print(toml_types.get(python_type, 'Other'))
            elif output_type == 'xml':
                print(xml_types.get(python_type, 'xs:any'))
            elif output_type in ["ini", "env", "python"]:
                print(python_type)
            else:
                raise CLIError(f"Unsupported output type {output_type}, try YAML, JSON, TOML, XML, or Python",
                               cli_tool=CLIError.CLITool.OBJ_GET)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_TYPE)

def obj_search(args):
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)

            paths = r.search_path(args.key)

            dump_type = args.OUTPUT_TYPE.lower()

            if dump_type == 'json':
                print(json.dumps(paths))
            elif dump_type == 'yaml':
                print(yaml.safe_dump(paths))
            elif dump_type == 'list':
                for p in paths:
                    print(p)
            else:
                raise CLIError(f"Unsupported dump type {dump_type}, only YAML, JSON, and LIST", cli_tool=CLIError.CLITool.OBJ_SEARCH)


    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_SEARCH)

def obj_func(args):
    def guess_parse(param_value):
        try:
            return ast.literal_eval(param_value)
        except Exception as exc:
            raise TypeError(f"Could not guess the parameter type, {exc}")
    def parse_type(type_name, param_value):
        type_name = type_name.strip().lower()
        if type_name == 'str':
            return str(param_value)
        elif type_name == 'int':
            try:
                return int(param_value)
            except:
                raise TypeError(f"Value '{param_value}' does not match type int")
        elif type_name == 'float':
            try:
                return float(param_value)
            except:
                raise TypeError(f"Value '{param_value}' does not match type int")
        elif type_name == 'bool':
            if param_value.strip().lower() == 'true':
                return True
            if param_value.strip().lower() == 'false':
                return False
            raise TypeError(f"Value '{param_value}' does not match type bool")
        elif type_name == 'list' or type_name == 'dict':
            try:
                return ast.literal_eval(param_value)
            except Exception as exc:
                raise TypeError(f"Could not guess the parameter type, {exc}")
        else:
            raise ValueError('Could not interpret type, only str, int, float, bool, list, dict accepted.')

    try:
        re_pat = re.compile(r"(.+?)=(.+)")
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = UnsafeRickle(_input, load_lambda=args.LOAD_LAMBDA)
            dump_type = args.OUTPUT_TYPE.lower()

            params = dict()
            if args.params:
                for p in args.params:
                    m = re_pat.match(p)
                    param_name = m.group(1)
                    param_value = m.group(2)
                    if ':' in param_name:
                        param_name, ptype = param_name.split(':')
                        param_value = parse_type(ptype, param_value)
                    elif args.infer:
                        param_value = guess_parse(param_value)

                    params[param_name] = param_value
            v = r(args.key, **params)

            if not v is None:
                if isinstance(v, Rickle):
                    if dump_type == 'json':
                        print(v.to_json())
                    elif dump_type == 'toml':
                        print(v.to_toml())
                    elif dump_type == 'xml':
                        print(v.to_xml())
                    elif dump_type == 'ini':
                        print(v.to_ini())
                    else:
                        print(v.to_yaml())
                elif isinstance(v, dict):
                    if dump_type == 'json':
                        print(json.dumps(v))
                    elif dump_type == 'toml':
                        print(tomlw.dumps(v))
                    elif dump_type == 'ini':
                        print(Rickle(v).to_ini())
                    elif dump_type == 'xml':
                        if importlib.util.find_spec('xmltodict'):
                            import xmltodict
                            print(xmltodict.unparse(input_dict=v, pretty=True))
                    else:
                        print(yaml.safe_dump(v))
                else:
                    print(v)
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_FUNC)


def serve(args):
    try:
        from rickled.net import serve_rickle_http
    except NameError:
        warnings.warn('Required Python package "twisted" not found.', ImportWarning)
        return

    try:
        if args.UNSAFE:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            rick = UnsafeRickle(_input, load_lambda=args.LOAD_LAMBDA, RICKLE_PATH_SEP='/')
        else:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            rick = Rickle(_input, load_lambda=args.LOAD_LAMBDA, RICKLE_PATH_SEP='/')

        if args.b:
            import webbrowser

            scheme = 'https' if args.CERTIFICATE and args.PRIVATE_KEY else 'http'
            webbrowser.open(f'{scheme}://{args.HOST}:{args.PORT}', new=2)

        serve_rickle_http(rickle=rick,
                          port=args.PORT,
                          interface=args.HOST,
                          serialised=args.s,
                          output_type=args.OUTPUT_TYPE,
                          path_to_certificate=args.CERTIFICATE,
                          path_to_private_key=args.PRIVATE_KEY,
                        )
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SERVE)

def check(args):
    try:
        if args.INPUT:
            Schema(input_files=args.INPUT,
                   input_directories=[args.INPUT_DIRECTORY],
                   schema=args.SCHEMA,
                   output_dir=args.FAIL_DIRECTORY,
                   verbose=args.VERBOSE,
                   silent=args.SILENT).do_validation()
        else:
            data = sys.stdin.read()
            input_data = Converter.infer_read_string_type(data)

            schema = Converter.infer_read_file_type(args.SCHEMA)

            passed = Schema.schema_validation(input_data, schema, no_print=not args.VERBOSE)

            if not args.SILENT:
                result = f"{cli_bcolors.OKGREEN}OK{cli_bcolors.ENDC}" if passed else f"{cli_bcolors.FAIL}FAIL{cli_bcolors.ENDC}"
                print(f"{cli_bcolors.OKBLUE}INPUT{cli_bcolors.ENDC} -> {result}")

            if not passed:
                sys.exit(1)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_CHECK)

def gen(args):
    try:
        if args.INPUT:
            Schema(input_files=args.INPUT,
                   input_directories=[args.INPUT_DIRECTORY],
                   output_files=args.OUTPUT,
                   silent=args.SILENT,
                   default_output_type=args.OUTPUT_TYPE).do_generation()
        else:
            data = sys.stdin.read()
            input_data = Converter.infer_read_string_type(data)

            schema_dict = Schema.generate_schema_from_obj(input_data)

            ttype = args.OUTPUT_TYPE.lower().strip()


            if ttype == 'yaml':
                print(yaml.dump(schema_dict))
            elif ttype == 'json':
                print(json.dumps(schema_dict))
            elif ttype == 'toml':
                print(tomlw.dumps(toml_null_stripper(schema_dict)))
            elif ttype == 'xml' and importlib.util.find_spec('xmltodict'):
                import xmltodict
                print(xmltodict.unparse({'schema':schema_dict}, pretty=True))
            elif ttype == 'ini' or ttype == '.env':
                raise CLIError(message='INI and .ENV output unsupported for schema generation', cli_tool=CLIError.CLITool.SCHEMA_GEN)
            else:
                raise CLIError(message=f'Unknown type "{ttype}"', cli_tool=CLIError.CLITool.SCHEMA_GEN)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_GEN)

def main():

    supported_list = f"""
- {cli_bcolors.OKBLUE}YAML (r/w){cli_bcolors.ENDC}
- {cli_bcolors.OKBLUE}JSON (r/w){cli_bcolors.ENDC}
- {cli_bcolors.OKBLUE}TOML (r/w){cli_bcolors.ENDC}
- {cli_bcolors.OKBLUE}INI (r/w){cli_bcolors.ENDC}"""

    if importlib.util.find_spec('dotenv'):
        supported_list = f"{supported_list}\n- {cli_bcolors.OKBLUE}ENV (r){cli_bcolors.ENDC}"
    if importlib.util.find_spec('xmltodict'):
        supported_list = f"{supported_list}\n- {cli_bcolors.OKBLUE}XML (r/w){cli_bcolors.ENDC}"


    parser = argparse.ArgumentParser(
        prog='rickle',
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"""
---------------------------------------------------------------------------------------------{cli_bcolors.OKGREEN}
██████╗ ██╗ ██████╗██╗  ██╗██╗     ███████╗
██╔══██╗██║██╔════╝██║ ██╔╝██║     ██╔════╝
██████╔╝██║██║     █████╔╝ ██║     █████╗  
██╔══██╗██║██║     ██╔═██╗ ██║     ██╔══╝  
██║  ██║██║╚██████╗██║  ██╗███████╗███████╗
╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝{cli_bcolors.ENDC}

{cli_bcolors.HEADER}YAML (+JSON, TOML...) tools for Python{cli_bcolors.ENDC} (version {ver}).
---------------------------------------------------------------------------------------------
Supported file types ({cli_bcolors.OKBLUE}-t{cli_bcolors.ENDC}) include:
{supported_list}
---------------------------------------------------------------------------------------------
""",
        epilog=f"""
---------------------------------------------------------------------------------------------
\nFor usage examples, visit:\n{cli_bcolors.UNDERLINE}{GITHUB_DOCS_URL}{cli_bcolors.ENDC}\n\n
---------------------------------------------------------------------------------------------
        """
    )
    parser.add_argument(
        "--version",
        "-v",
        help="show version number",
        action="version",
        version=f'%(prog)s {ver}'
    )

    subparsers = parser.add_subparsers()

    #################### CONV #####################
    # ░░      ░░░      ░░   ░░░  ░  ░░░░  ░
    # ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒    ▒▒  ▒  ▒▒▒▒  ▒
    # ▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓  ▓  ▓  ▓▓  ▓▓  ▓▓
    # █  ████  █  ████  █  ██    ███    ███
    # ██      ███      ██  ███   ████  ████


    parser_conv = subparsers.add_parser('conv',
                                        help=f'{cli_bcolors.OKBLUE}Converting{cli_bcolors.ENDC} files between formats',
                                        formatter_class=argparse.RawTextHelpFormatter,
                                        description=f"""
{cli_bcolors.HEADER}Tool for converting files to or from different formats{cli_bcolors.ENDC}.
If input is piped, output is printed. For INPUT or INPUT_DIRECTORY output is written to file(s).

Examples: 

    $ cat config.yaml | rickle conv --output-type JSON
    $ rickle conv --input conf1.yaml conf2.yaml  --output-type JSON
    
When no output type is defined, the file extension (suffix) is used to infer the output type.    

    $ rickle conv --input conf1.yaml --output config.toml

Supported formats: 
{Converter.supported}
    """)

    parser_conv.add_argument('--input',
                             dest='INPUT',
                             type=str,
                             help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to convert",
                             nargs='+',
                             metavar='',
                             default=None)
    parser_conv.add_argument('--input-directory',
                             dest='INPUT_DIRECTORY',
                             type=str,
                             metavar='',
                             help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC} of input files",
                             default=None)
    parser_conv.add_argument('--output',
                             dest='OUTPUT',
                             type=str,
                             metavar='',
                             help=f"{cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC} names, only if --input given",
                             nargs='+',
                             default=None)
    parser_conv.add_argument('--output-type',
                             dest='OUTPUT_TYPE',
                             type=str,
                             metavar='',
                             help=f"output {cli_bcolors.OKBLUE}file type{cli_bcolors.ENDC} (default = YAML)",
                             default='yaml')
    parser_conv.add_argument('--input-type',
                             dest='INPUT_TYPE',
                             type=str,
                             metavar='',
                             help=f"optional input {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (type inferred if none)",
                             default=None)
    parser_conv.add_argument('--verbose',
                             '-v',
                             dest='VERBOSE',
                             action='store_true',
                             help=f"{cli_bcolors.OKBLUE}verbose{cli_bcolors.ENDC} output", )

    parser_conv.set_defaults(func=conv)

    #################### OBJ #####################
    # ░░      ░░       ░░        ░
    # ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒▒▒▒▒▒  ▒
    # ▓  ▓▓▓▓  ▓       ▓▓▓▓▓▓▓▓  ▓
    # █  ████  █  ████  █  ████  █
    # ██      ██       ███      ██


    parser_obj = subparsers.add_parser('obj',
                                       help=f'Tool for reading or editing {cli_bcolors.OKBLUE} objects {cli_bcolors.ENDC}',
                                       formatter_class=argparse.RawTextHelpFormatter,
                                       description=f"""
{cli_bcolors.HEADER}Tool for reading or editing files in different formats{cli_bcolors.ENDC}.
Input is used to create a Rickle {cli_bcolors.HEADER}object{cli_bcolors.ENDC} which can then be queried and further modified.
        """,
                                       )

    parser_obj.add_argument('--input',
                            dest='INPUT',
                            type=str,
                            metavar='',
                            help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC} to create object from",
                            default=None)
    parser_obj.add_argument('--output',
                            dest='OUTPUT',
                            type=str,
                            metavar='',
                            help=f"write to {cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC}",
                            required=False)
    parser_obj.add_argument('--output-type',
                            dest='OUTPUT_TYPE',
                            type=str,
                            metavar='',
                            help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (default = YAML)",
                            default='yaml')
    parser_obj.add_argument('--load-lambda',
                            dest='LOAD_LAMBDA',
                            action='store_true',
                            help=f"load {cli_bcolors.OKBLUE}lambda{cli_bcolors.ENDC} types",
                            default=False)

    subparsers_obj = parser_obj.add_subparsers()

    #################### OBJ - GET #####################
    #   ___ ___ _____
    #  / __| __|_   _|
    # | (_ | _|  | |
    #  \___|___| |_|

    get_obj_parser = subparsers_obj.add_parser('get',
                                               help=f'{cli_bcolors.OKBLUE}Getting{cli_bcolors.ENDC} values from objects',
                                               formatter_class=argparse.RawTextHelpFormatter,
                                               description=f"""
{cli_bcolors.HEADER}Tool for getting values from objects{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle obj get /path/to
    $ rickle obj --input conf1.yaml --output-type JSON get /path/to  
    
""",)

    get_obj_parser.add_argument('key',
                                type=str,
                                help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} (path) to get value",
                                metavar='key')

    get_obj_parser.set_defaults(func=obj_get)

    #################### OBJ - SET #####################
    #  ___ ___ _____
    # / __| __|_   _|
    # \__ \ _|  | |
    # |___/___| |_|

    set_obj_parser = subparsers_obj.add_parser('set',
                                               formatter_class=argparse.RawTextHelpFormatter,
                                               help=f'{cli_bcolors.OKBLUE}Setting{cli_bcolors.ENDC} values in objects',
                                               description=f"""
{cli_bcolors.HEADER}Tool for setting values in objects{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle obj set /path/to new_value
    $ rickle obj --input conf1.yaml --output-type JSON set /path/to new_value  
    
""",
                                               )

    set_obj_parser.add_argument('key',
                                type=str,
                                help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to set value",
                                metavar='key')
    set_obj_parser.add_argument('value',
                                type=str,
                                help=f"{cli_bcolors.OKBLUE}Value{cli_bcolors.ENDC} to set",
                                metavar='value')

    set_obj_parser.set_defaults(func=obj_set)

    #################### OBJ - DEL #####################
    #  ___  ___ _
    # |   \| __| |
    # | |) | _|| |__
    # |___/|___|____|

    del_obj_parser = subparsers_obj.add_parser('del',
                                               formatter_class=argparse.RawTextHelpFormatter,
                                               help=f'For {cli_bcolors.OKBLUE}deleting{cli_bcolors.ENDC} keys (paths) in objects',
                                               description=f"""
{cli_bcolors.HEADER}Tool for deleting keys (paths) in objects{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle obj del /path/to 
""",)

    del_obj_parser.add_argument('key',
                                type=str,
                                help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to delete",
                                metavar='key')

    del_obj_parser.set_defaults(func=obj_del)

    #################### OBJ - TYPE #####################
    #  _______   _____ ___
    # |_   _\ \ / / _ \ __|
    #   | |  \ V /|  _/ _|
    #   |_|   |_| |_| |___|

    type_obj_parser = subparsers_obj.add_parser('type',
                                                formatter_class=argparse.RawTextHelpFormatter,
                                                help=f'Printing value {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} ',
                                                description=f"""
{cli_bcolors.HEADER}Tool for printing the type of the value for a key in the object{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle obj type /path/to 
    
Types depend on --output-type and can be the following:

    Python |    YAML |    JSON |      TOML |            XML |
    =========================================================
    str    |     str |  string |    String |      xs:string |
    int    |     int |  number |   Integer |     xs:integer |
    float  |   float |  number |     Float |     xs:decimal |
    bool   | boolean | boolean |   Boolean |     xs:boolean |
    list   |     seq |   array |     Array |    xs:sequence |
    dict   |     map |  object | Key/Value | xs:complexType |
    bytes  |  binary |         |           |                |
    ---------------------------------------------------------
    *      |  Python |  object |     Other |         xs:any |

""",)

    type_obj_parser.add_argument('key',
                                 type=str,
                                 help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to print value type",
                                 metavar='key')

    type_obj_parser.set_defaults(func=obj_type)

    #################### OBJ - SEARCH #####################
    #  ___ ___   _   ___  ___ _  _
    # / __| __| /_\ | _ \/ __| || |
    # \__ \ _| / _ \|   / (__| __ |
    # |___/___/_/ \_\_|_\\___|_||_|

    search_obj_parser = subparsers_obj.add_parser('search',
                                                  formatter_class=argparse.RawTextHelpFormatter,
                                                  help=f'For {cli_bcolors.OKBLUE}searching{cli_bcolors.ENDC} keys (paths) in objects',
                                                  description=f"""
{cli_bcolors.HEADER}Tool for searching keys in objects{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle obj search /path/to 
    
Only the following --output-type is allowed: YAML, JSON, and LIST. Using LIST will only print the path(s).


""",)

    search_obj_parser.add_argument('key',
                                   type=str,
                                   help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to search",
                                   metavar='key')

    search_obj_parser.set_defaults(func=obj_search)

    #################### OBJ - FUNC #####################
    #  ___ _   _ _  _  ___
    # | __| | | | \| |/ __|
    # | _|| |_| | .` | (__
    # |_|  \___/|_|\_|\___|

    func_obj_parser = subparsers_obj.add_parser('func',
                                                formatter_class=argparse.RawTextHelpFormatter,
                                                help=f'Executing {cli_bcolors.OKBLUE}functions{cli_bcolors.ENDC} defined in objects',
                                                description=f"""
{cli_bcolors.HEADER}Tool for executing functions defined in objects{cli_bcolors.ENDC}.
To enable unsafe usage, the environment variable {cli_bcolors.WARNING}RICKLE_UNSAFE_LOAD{cli_bcolors.ENDC} must be set and {cli_bcolors.WARNING}--load-lambda{cli_bcolors.ENDC} passed.  

Examples: 

    $ export RICKLE_UNSAFE_LOAD=1 
    $ cat config.yaml | rickle obj --load-lambda func /path/to param1:int=1 param2:str=2 
    
Every param needs to have an explicit type, indicated by a colon and the Python type name:

    - int    - str
    - float  - list
    - bool   - dict
    
Examples: 

    $ cat app.yaml | rickle obj --load-lambda func /path/to things:list="['foo','bar']"

This will pass a list called "things". To automatically infer the types, use --infer:

    $ cat app.yaml | rickle obj --load-lambda func /path/to --infer things="['foo','bar']"

This will infer input params. 

{cli_bcolors.WARNING}There are major security risks involved in using this functionality!{cli_bcolors.ENDC}

{cli_bcolors.FAIL}{cli_bcolors.BOLD}{cli_bcolors.UNDERLINE}Warning: Only use on trusted sources (files, urls, etc.){cli_bcolors.ENDC}
""",)

    func_obj_parser.add_argument('--infer',
                                 action='store_true',
                                 help=f"{cli_bcolors.OKBLUE}infer parameter{cli_bcolors.ENDC} types",
                                 default=False)
    func_obj_parser.add_argument('key',
                                 type=str,
                                 help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} (name) of function",
                                 metavar='key')
    func_obj_parser.add_argument('params',
                                 type=str,
                                 help=f"{cli_bcolors.OKBLUE}Params{cli_bcolors.ENDC} for function",
                                 metavar='params', nargs='+')

    func_obj_parser.set_defaults(func=obj_func)


    #################### SERVE #####################
    # ░░      ░░        ░       ░░  ░░░░  ░        ░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒
    # ▓▓      ▓▓      ▓▓▓       ▓▓▓  ▓▓  ▓▓      ▓▓▓
    # ███████  █  ███████  ███  ████    ███  ███████
    # ██      ██        █  ████  ████  ████        █

    if importlib.util.find_spec('twisted'):

        parser_serve = subparsers.add_parser('serve',
                                             help=f'Serving objects through {cli_bcolors.OKBLUE}http(s){cli_bcolors.ENDC}',
                                             formatter_class=argparse.RawTextHelpFormatter,
                                             description=f"""
{cli_bcolors.HEADER}Tool for serving objects through http(s){cli_bcolors.ENDC}.
By default served as JSON. The path separator is set to / as default. 

Examples: 

    $ cat app.yaml | rickle serve
    
The host and port can be specified:

    $ cat app.yaml | rickle serve --host localhost --port 8087

Adding --private-key and --certificate will serve the object over SSL:
 
    $ cat app.yaml | rickle serve --private-key my_local.pem --certificate my_local.crt

Unsafe usage like functions can be enabled:

    $ export RICKLE_UNSAFE_LOAD=1 
    $ cat app.yaml | rickle serve --load-lambda --unsafe 
    
{cli_bcolors.WARNING}There are major security risks involved in using this functionality!{cli_bcolors.ENDC}

{cli_bcolors.FAIL}{cli_bcolors.BOLD}{cli_bcolors.UNDERLINE}Warning: Only use on trusted sources (files, urls, etc.){cli_bcolors.ENDC}
""",)

        parser_serve.add_argument('--input',
                                  dest="INPUT",
                                  type=str,
                                  help=f"{cli_bcolors.OKBLUE}input{cli_bcolors.ENDC} file to serve",
                                  default=None,
                                  metavar='')
        # TODO implement config
        # parser_serve.add_argument('--config',
        #                           dest='CONFIG',
        #                           type=str,
        #                           help=f"{cli_bcolors.OKBLUE}config{cli_bcolors.ENDC} file path",
        #                           default=None,
        #                           metavar='')
        parser_serve.add_argument('--host',
                                  dest='HOST',
                                  type=str,
                                  help=f"{cli_bcolors.OKBLUE}host address{cli_bcolors.ENDC} (default = localhost)",
                                  default='localhost',
                                  metavar=''
                                  )
        parser_serve.add_argument('--port',
                                  dest="PORT",
                                  type=int,
                                  help=f"{cli_bcolors.OKBLUE}port{cli_bcolors.ENDC} number (default = 8080)",
                                  default=8080,
                                  metavar='')
        parser_serve.add_argument('--private-key',
                                  dest='PRIVATE_KEY',
                                  type=str,
                                  help=f"{cli_bcolors.OKBLUE}private key{cli_bcolors.ENDC} file path",
                                  default=None,
                                  metavar='')
        parser_serve.add_argument('--certificate',
                                  dest='CERTIFICATE',
                                  type=str,
                                  help=f"ssl {cli_bcolors.OKBLUE}certificate{cli_bcolors.ENDC} file path",
                                  default=None,
                                  metavar='')
        parser_serve.add_argument('--output-type',
                                  dest="OUTPUT_TYPE",
                                  type=str,
                                  help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (default = JSON)",
                                  default='json',
                                  metavar='')
        parser_serve.add_argument('--load-lambda',
                                  dest="LOAD_LAMBDA",
                                  action='store_true',
                                  help=f"load {cli_bcolors.OKBLUE}lambda{cli_bcolors.ENDC} true",
                                  default=False)

        parser_serve.add_argument('--unsafe',
                                  dest="UNSAFE",
                                  action='store_true',
                                  help=f"load {cli_bcolors.OKBLUE}UnsafeRickle{cli_bcolors.ENDC} ({cli_bcolors.FAIL}VERY UNSAFE{cli_bcolors.ENDC})",
                                  default=False,)

        parser_serve.add_argument('--browser',
                                  '-b',
                                  action='store_true',
                                  help=f"open {cli_bcolors.OKBLUE}browser{cli_bcolors.ENDC}", )
        parser_serve.add_argument('--serialised',
                                  '-s',
                                  action='store_true',
                                  help=f"serve as {cli_bcolors.OKBLUE}serialised{cli_bcolors.ENDC} data (default = false)",
                                  default=False)


        parser_serve.set_defaults(func=serve)

    #################### SCHEMA #####################
    # ░░      ░░░      ░░  ░░░░  ░        ░  ░░░░  ░░      ░░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒   ▒▒   ▒  ▒▒▒▒  ▒
    # ▓▓      ▓▓  ▓▓▓▓▓▓▓        ▓      ▓▓▓        ▓  ▓▓▓▓  ▓
    # ███████  █  ████  █  ████  █  ███████  █  █  █        █
    # ██      ███      ██  ████  █        █  ████  █  ████  █


    parser_schema = subparsers.add_parser('schema',
                                          help=f'Generating and checking {cli_bcolors.OKBLUE}schemas{cli_bcolors.ENDC} of YAML files',
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          description=f"""
{cli_bcolors.HEADER}Tool for generating and checking schemas of several different formats{cli_bcolors.ENDC}.

Supported formats: 
{Schema.supported}
""",)

    schema_subparsers = parser_schema.add_subparsers()

    #################### SCHEMA - CHECK ############
    #   ___ _  _ ___ ___ _  __
    #  / __| || | __/ __| |/ /
    # | (__| __ | _| (__| ' <
    #  \___|_||_|___\___|_|\_\

    parser_schema_check = schema_subparsers.add_parser('check',
                                                       help=f'{cli_bcolors.OKBLUE}Checking{cli_bcolors.ENDC} schemas of files',
                                                       formatter_class=argparse.RawTextHelpFormatter,
                                                       description=f"""
{cli_bcolors.HEADER}Tool for checking schemas of files{cli_bcolors.ENDC}.

Examples: 

    $ cat config.yaml | rickle schema check --schema config.schema.yaml
    
Which will print OK or FAIL depending on success. For more detailed output the --verbose option can be used:

    $ cat config.yaml | rickle schema check --schema config.schema.yaml --verbose
    
To silence the OK/FAIL output, --silence can be used. If input is piped and the check fails, exit code 1 is returned.
""",)


    parser_schema_check.add_argument('--input',
                                     dest='INPUT',
                                     type=str,
                                     help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to check",
                                     nargs='+',
                                     metavar='')
    parser_schema_check.add_argument('--input-directory',
                                     type=str,
                                     dest='INPUT_DIRECTORY',
                                     help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC}(s) of files to check",
                                     default=None,
                                     metavar='')

    parser_schema_check.add_argument('--schema',
                                     dest='SCHEMA',
                                     type=str,
                                     help=f"{cli_bcolors.OKBLUE}schema definition file{cli_bcolors.ENDC} to compare",
                                     metavar='',
                                     )

    parser_schema_check.add_argument('--fail-directory',
                                     dest='FAIL_DIRECTORY',
                                     type=str,
                                     help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC} to move failed files to",
                                     metavar='')

    parser_schema_check.add_argument('--verbose',
                                     '-v',
                                     dest='VERBOSE',
                                     action='store_true',
                                     help=f"{cli_bcolors.OKBLUE}verbose{cli_bcolors.ENDC} output", )
    parser_schema_check.add_argument('--silent',
                                     '-s',
                                     dest='SILENT',
                                     action='store_true',
                                     help=f"{cli_bcolors.OKBLUE}silence{cli_bcolors.ENDC} output", )

    parser_schema_check.set_defaults(func=check)

    #################### SCHEMA - GEN ############
    #   ___ ___ _  _
    #  / __| __| \| |
    # | (_ | _|| .` |
    #  \___|___|_|\_|

    parser_schema_gen = schema_subparsers.add_parser('gen',
                                                     help=f'Tool for {cli_bcolors.OKBLUE}generating{cli_bcolors.ENDC} schemas of files',
                                                     formatter_class=argparse.RawTextHelpFormatter,
                                                     description=f"""
{cli_bcolors.HEADER}Tool for generating schemas of files{cli_bcolors.ENDC}.
Generates schemas from input. 

Examples: 

    $ cat config.yaml | rickle schema gen  
    
If --input or --input-directory are passed the output will be to files. If piped, the output is printed.
""",)

    parser_schema_gen.add_argument('--input',
                                   dest='INPUT',
                                   type=str,
                                   help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to generate from",
                                   nargs='+',
                                   metavar='')
    parser_schema_gen.add_argument('--output',
                                   dest='OUTPUT',
                                   type=str,
                                   help=f"{cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC}(s) to write to",
                                   nargs='+',
                                   metavar='')
    parser_schema_gen.add_argument('--input-directory',
                                   dest='INPUT_DIRECTORY',
                                   type=str,
                                   help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC}(s) of files to generate from",
                                   default=None,
                                   metavar='')
    parser_schema_gen.add_argument('--output-type',
                                   dest='OUTPUT_TYPE',
                                   type=str,
                                   help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (default = YAML)",
                                   default='yaml',
                                   metavar='')
    parser_schema_gen.add_argument('--silent',
                                   '-s',
                                   dest='SILENT',
                                   action='store_true',
                                   help=f"{cli_bcolors.OKBLUE}silence{cli_bcolors.ENDC} output", )

    parser_schema_gen.set_defaults(func=gen)

    #################################################
    # Making a bit more friendly for debugging
    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help(sys.stderr)
        sys.exit(2)
    except CLIError as cli_exc:
        sys.stderr.write(f'\n{cli_bcolors.FAIL}error: {cli_exc.message}{cli_bcolors.ENDC}\n\n')
        if cli_exc.cli_tool == CLIError.CLITool.CONV:
            parser_conv.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ:
            parser_obj.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.SERVE:
            parser_serve.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.SCHEMA:
            parser_schema.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_GET:
            get_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_SET:
            set_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_DEL:
            del_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_TYPE:
            type_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_SEARCH:
            search_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.OBJ_FUNC:
            func_obj_parser.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.SCHEMA_CHECK:
            parser_schema_check.print_help(sys.stderr)
        elif cli_exc.cli_tool == CLIError.CLITool.SCHEMA_GEN:
            parser_schema_gen.print_help(sys.stderr)
        else:
            parser.print_help(sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()