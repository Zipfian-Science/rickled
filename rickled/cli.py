# ASCCI Text found in this file was generated on
# https://patorjk.com/software/taag/
# Large heading using "Shaded Blocky" font
# Sub headings using "Small" font
import sys
import warnings
from enum import Enum

import rickled.__version__ as ver
import argparse
from rickled.tools import cli_bcolors
from rickled.tools import Schema
from rickled.tools import Converter
from rickled.tools import toml_null_stripper

from rickled import Rickle
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


def conv(args):
    try:
        Converter(input_files=args.i,
                  output_files=args.o,
                  input_directories=args.d,
                  default_output_type=args.t,
                  silent=args.s).do_convert()
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.CONV)

def obj_get(args):
    try:
        if args:
            r = Rickle(args.i, load_lambda=args.l)
            v = r.get(args.key)
            dump_type = args.t.lower()

            if isinstance(v, Rickle):
                v = toml_null_stripper(v.dict())
            if isinstance(v, dict):
                v = toml_null_stripper(v)
            elif v is None:
                v = ''

            if args.o:

                if dump_type == 'json':
                    with open(args.o, 'w') as fp:
                        json.dump(v, fp)
                elif dump_type == 'toml':
                    with open(args.o, 'wb') as fp:
                        tomlw.dump(v, fp)
                else:
                    with open(args.o, 'w') as fp:
                        yaml.safe_dump(v, fp)


            else:
                if dump_type == 'json':
                    print(json.dumps(v))
                elif dump_type == 'toml':
                    print(tomlw.dumps(v))
                else:
                    print(yaml.safe_dump(v))


    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_GET)



def obj_set(args):
    try:
        if args:
            r = Rickle(args.i)
            r.set(args.key, args.value)
            dump_type = args.t.lower()

            if args.o:
                if dump_type == 'json':
                    r.to_json(output=args.o)
                elif dump_type == 'toml':
                    r.to_toml(output=args.o)
                else:
                    r.to_yaml(output=args.o)
            else:
                if dump_type == 'json':
                    print(r.to_json())
                elif dump_type == 'toml':
                    print(r.to_toml())
                else:
                    print(r.to_yaml())
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_SET)


def obj_del(args):
    try:
        if args:
            r = Rickle(args.i)
            r.remove(args.key)
            dump_type = args.t.lower()

            if args.o:
                if dump_type == 'json':
                    r.to_json(output=args.o)
                elif dump_type == 'toml':
                    r.to_toml(output=args.o)
                else:
                    r.to_yaml(output=args.o)
            else:
                if dump_type == 'json':
                    print(r.to_json())
                elif dump_type == 'toml':
                    print(r.to_toml())
                else:
                    print(r.to_yaml())
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_DEL)

def obj_type(args):
    try:
        if args:
            r = Rickle(args.i, load_lambda=args.l)
            v = r.get(args.key)
            print(type(v))
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_TYPE)

def obj_search(args):
    try:
        if args:
            r = Rickle(args.i, load_lambda=args.l)
            paths = r.search_path(args.key)
            for p in paths:
                print(p)
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
            r = Rickle(args.i, load_lambda=args.l)
            dump_type = args.t.lower()

            params = dict()
            if args.params:
                for p in args.params:
                    m = re_pat.match(p)
                    param_name = m.group(1)
                    param_value = m.group(2)
                    if ':' in param_name:
                        param_name, ptype = param_name.split(':')
                        param_value = parse_type(ptype, param_value)
                    elif args.x:
                        param_value = guess_parse(param_value)

                    params[param_name] = param_value
            v = r(args.key, **params)

            if not v is None:
                if isinstance(v, Rickle):
                    if dump_type == 'json':
                        print(v.to_json())
                    elif dump_type == 'toml':
                        print(v.to_toml())
                    else:
                        print(v.to_yaml())
                elif isinstance(v, dict):
                    if dump_type == 'json':
                        print(json.dumps(v))
                    elif dump_type == 'toml':
                        print(tomlw.dumps(v))
                    else:
                        print(yaml.safe_dump(v))
                else:
                    print(v)
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_FUNC)


def serve(args):
    try:
        from rickled.net import serve_rickle_http, serve_rickle_https
    except NameError:
        warnings.warn('Required Python package "twisted" not found.', ImportWarning)
        return

    try:
        rick = Rickle(args.i)

        if args.b:
            import webbrowser
            host = 'localhost' if args.a == '' else args.a
            scheme = 'https' if args.c and args.k else 'http'
            webbrowser.open(f'{scheme}://{host}:{args.p}', new=2)

        if args.c and args.k:
            serve_rickle_https(rickle=rick,
                               path_to_certificate=args.c,
                               path_to_private_key=args.k,
                               port=args.p,
                               interface=args.a,
                               serialised=args.s,
                               output_type=args.t
                               )
        else:
            serve_rickle_http(rickle=rick,
                              port=args.p,
                              interface=args.a,
                              serialised=args.s,
                              output_type=args.t
                              )
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SERVE)

def check(args):
    try:
        Schema(input_files=args.i,
               input_directories=args.d,
               schema=args.c,
               output_dir=args.o,
               silent=args.s).do_validation()
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_CHECK)

def gen(args):
    try:
        Schema(input_files=args.i,
               input_directories=args.d,
               output_files=args.o,
               silent=args.s,
               default_output_type=args.t).do_generation()
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_GEN)

def main():
    parser = argparse.ArgumentParser(
        prog='rickle',
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
- {cli_bcolors.OKBLUE}YAML{cli_bcolors.ENDC}
- {cli_bcolors.OKBLUE}JSON{cli_bcolors.ENDC}
- {cli_bcolors.OKBLUE}TOML{cli_bcolors.ENDC}
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
                                        help=f'{cli_bcolors.OKBLUE}Converting{cli_bcolors.ENDC} files to or from YAML',
                                        description=f"""

{cli_bcolors.HEADER}Tool for converting files to or from YAML{cli_bcolors.ENDC}.
    """, )

    parser_conv.add_argument('-i', type=str, help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to convert",
                             nargs='+', metavar='input')
    parser_conv.add_argument('-d', type=str, help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC}(s) of input files",
                             default=None, nargs='+', metavar='dir')
    parser_conv.add_argument('-o', type=str, help=f"{cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC} names",
                             nargs='+', metavar='output')
    parser_conv.add_argument('-t', type=str, help=f"default output {cli_bcolors.OKBLUE}file type{cli_bcolors.ENDC} (JSON, YAML)",
                             default='yaml', metavar='type')
    parser_conv.add_argument('-s', action='store_true', help=f"{cli_bcolors.OKBLUE}suppress{cli_bcolors.ENDC} verbose output", )

    parser_conv.set_defaults(func=conv)

    #################### OBJ #####################
    # ░░      ░░       ░░        ░
    # ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒▒▒▒▒▒  ▒
    # ▓  ▓▓▓▓  ▓       ▓▓▓▓▓▓▓▓  ▓
    # █  ████  █  ████  █  ████  █
    # ██      ██       ███      ██


    parser_obj = subparsers.add_parser('obj',
                                       help=f'Tool for {cli_bcolors.OKBLUE}accessing/manipulating{cli_bcolors.ENDC} YAML files',
                                       description=f"""

    {cli_bcolors.HEADER}Tool for accessing/manipulating YAML files{cli_bcolors.ENDC}.
        """,
                                       )

    parser_obj.add_argument('-i', type=str, help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC} to read/modify",
                            metavar='input', required=True)
    parser_obj.add_argument('-o', type=str, help=f"{cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC} to save modified",
                            metavar='output', required=False)
    parser_obj.add_argument('-t', type=str,
                            help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (JSON, YAML)",
                            default='yaml', metavar='type')
    parser_obj.add_argument('-l', action='store_true', help=f"load {cli_bcolors.OKBLUE}lambda{cli_bcolors.ENDC} types",
                            default=False)

    subparsers_obj = parser_obj.add_subparsers()

    #################### OBJ - GET #####################
    #   ___ ___ _____
    #  / __| __|_   _|
    # | (_ | _|  | |
    #  \___|___| |_|

    get_obj_parser = subparsers_obj.add_parser('get',
                                               help=f'{cli_bcolors.OKBLUE}Getting{cli_bcolors.ENDC} values from YAML files',
                                               description=f"""

        {cli_bcolors.HEADER}Tool for getting values from YAML files{cli_bcolors.ENDC}.
            """,
                                               )

    get_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to get value",
                                metavar='key')

    get_obj_parser.set_defaults(func=obj_get)

    #################### OBJ - SET #####################
    #  ___ ___ _____
    # / __| __|_   _|
    # \__ \ _|  | |
    # |___/___| |_|

    set_obj_parser = subparsers_obj.add_parser('set',
                                               help=f'{cli_bcolors.OKBLUE}Setting{cli_bcolors.ENDC} values in YAML files',
                                               description=f"""

            {cli_bcolors.HEADER}Tool for setting values in YAML files{cli_bcolors.ENDC}.
                """,
                                               )

    set_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to set value",
                                metavar='key')
    set_obj_parser.add_argument('value', type=str, help=f"{cli_bcolors.OKBLUE}Value{cli_bcolors.ENDC} to set",
                                metavar='value')

    set_obj_parser.set_defaults(func=obj_set)

    #################### OBJ - DEL #####################
    #  ___  ___ _
    # |   \| __| |
    # | |) | _|| |__
    # |___/|___|____|

    del_obj_parser = subparsers_obj.add_parser('del',
                                               help=f'For {cli_bcolors.OKBLUE}deleting{cli_bcolors.ENDC} keys in YAML files',
                                               description=f"""

                {cli_bcolors.HEADER}Tool for deleting keys in YAML files{cli_bcolors.ENDC}.
                    """,
                                               )

    del_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to delete",
                                metavar='key')

    del_obj_parser.set_defaults(func=obj_del)

    #################### OBJ - TYPE #####################
    #  _______   _____ ___
    # |_   _\ \ / / _ \ __|
    #   | |  \ V /|  _/ _|
    #   |_|   |_| |_| |___|

    type_obj_parser = subparsers_obj.add_parser('type',
                                                help=f'Printing value {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} ',
                                                description=f"""

                    {cli_bcolors.HEADER}Tool for checking type of keys in YAML files{cli_bcolors.ENDC}.
                        """,
                                                )

    type_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to check",
                                 metavar='key')

    type_obj_parser.set_defaults(func=obj_type)

    #################### OBJ - SEARCH #####################
    #  ___ ___   _   ___  ___ _  _
    # / __| __| /_\ | _ \/ __| || |
    # \__ \ _| / _ \|   / (__| __ |
    # |___/___/_/ \_\_|_\\___|_||_|

    search_obj_parser = subparsers_obj.add_parser('search',
                                                  help=f'For {cli_bcolors.OKBLUE}searching{cli_bcolors.ENDC} key paths in YAML files',
                                                  description=f"""

                    {cli_bcolors.HEADER}Tool for searching keys in YAML files{cli_bcolors.ENDC}.
                        """,
                                                  )

    search_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} to search",
                                   metavar='key')

    search_obj_parser.set_defaults(func=obj_search)

    #################### OBJ - FUNC #####################
    #  ___ _   _ _  _  ___
    # | __| | | | \| |/ __|
    # | _|| |_| | .` | (__
    # |_|  \___/|_|\_|\___|

    func_obj_parser = subparsers_obj.add_parser('func',
                                                help=f'Executing {cli_bcolors.OKBLUE}function{cli_bcolors.ENDC} defined in YAML files',
                                                description=f"""

                    {cli_bcolors.HEADER}Tool for executing function defined in YAML files{cli_bcolors.ENDC}.
                        """,
                                                )

    func_obj_parser.add_argument('-x', action='store_true', help=f"{cli_bcolors.OKBLUE}infer parameter{cli_bcolors.ENDC} types",
                                 default=False)
    func_obj_parser.add_argument('key', type=str, help=f"{cli_bcolors.OKBLUE}Key{cli_bcolors.ENDC} (name) of function",
                                 metavar='key')
    func_obj_parser.add_argument('params', type=str, help=f"{cli_bcolors.OKBLUE}Params{cli_bcolors.ENDC} for function",
                                 metavar='params', nargs='+')

    func_obj_parser.set_defaults(func=obj_func)


    #################### SERVE #####################
    # ░░      ░░        ░       ░░  ░░░░  ░        ░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒
    # ▓▓      ▓▓      ▓▓▓       ▓▓▓  ▓▓  ▓▓      ▓▓▓
    # ███████  █  ███████  ███  ████    ███  ███████
    # ██      ██        █  ████  ████  ████        █


    parser_serve = subparsers.add_parser('serve',
                                         help=f'Serving YAML via {cli_bcolors.OKBLUE}http(s){cli_bcolors.ENDC}',
                                         description=f"""

    {cli_bcolors.HEADER}Tool for serving YAML via http(s){cli_bcolors.ENDC}.
        """,
                                         )

    parser_serve.add_argument('-i', type=str,
                              help=f"{cli_bcolors.OKBLUE}YAML{cli_bcolors.ENDC} or {cli_bcolors.OKBLUE}JSON{cli_bcolors.ENDC} file to serve",
                              metavar='file')
    # TODO implement config
    # parser_serve.add_argument('-c', type=str, help=f"{cli_bcolors.OKBLUE}config{cli_bcolors.ENDC} file path",
    #                           default=None, metavar='config')
    parser_serve.add_argument('-a', type=str, help=f"{cli_bcolors.OKBLUE}host address{cli_bcolors.ENDC}",
                              default='', metavar='address')
    parser_serve.add_argument('-p', type=int, help=f"{cli_bcolors.OKBLUE}port{cli_bcolors.ENDC} number",
                              default=8080, metavar='port')
    parser_serve.add_argument('-k', type=str, help=f"{cli_bcolors.OKBLUE}private key{cli_bcolors.ENDC} file path",
                              default=None, metavar='privkey')
    parser_serve.add_argument('-c', type=str, help=f"{cli_bcolors.OKBLUE}SSL certificate{cli_bcolors.ENDC} file path",
                              default=None, metavar='cert')
    parser_serve.add_argument('-b', action='store_true', help=f"open URL in {cli_bcolors.OKBLUE}browser{cli_bcolors.ENDC}", )
    parser_serve.add_argument('-s', action='store_true',
                              help=f"Serve as {cli_bcolors.OKBLUE}serialised{cli_bcolors.ENDC} data", )
    parser_serve.add_argument('-t', type=str,
                            help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (JSON, YAML)",
                            default='json', metavar='type')
    parser_serve.set_defaults(func=serve)

    #################### SCHEMA #####################
    # ░░      ░░░      ░░  ░░░░  ░        ░  ░░░░  ░░      ░░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒   ▒▒   ▒  ▒▒▒▒  ▒
    # ▓▓      ▓▓  ▓▓▓▓▓▓▓        ▓      ▓▓▓        ▓  ▓▓▓▓  ▓
    # ███████  █  ████  █  ████  █  ███████  █  █  █        █
    # ██      ███      ██  ████  █        █  ████  █  ████  █


    parser_schema = subparsers.add_parser('schema',
                                          help=f'Generating and checking {cli_bcolors.OKBLUE}schemas{cli_bcolors.ENDC} of YAML files',
                                          description=f"""

    {cli_bcolors.HEADER}Tool for generating and checking schemas of YAML files{cli_bcolors.ENDC}.
        """,
                                          )

    schema_subparsers = parser_schema.add_subparsers()

    #################### SCHEMA - CHECK ############
    #   ___ _  _ ___ ___ _  __
    #  / __| || | __/ __| |/ /
    # | (__| __ | _| (__| ' <
    #  \___|_||_|___\___|_|\_\

    parser_schema_check = schema_subparsers.add_parser('check',
                                                       help=f'{cli_bcolors.OKBLUE}Checking{cli_bcolors.ENDC} schemas of YAML files',
                                                       description=f"""

        {cli_bcolors.HEADER}Tool for checking schemas of YAML files{cli_bcolors.ENDC}.
            """,
                                                       )


    parser_schema_check.add_argument('-i', type=str, help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to check",
                                     nargs='+', metavar='input')
    parser_schema_check.add_argument('-d', type=str, help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC}(s) of files to check",
                                     default=None, nargs='+', metavar='dir')

    parser_schema_check.add_argument('-c', type=str, help=f"{cli_bcolors.OKBLUE}schema definition file{cli_bcolors.ENDC} to compare",
                                     metavar='schema')

    parser_schema_check.add_argument('-o', type=str,
                                     help=f"{cli_bcolors.OKBLUE}output directory{cli_bcolors.ENDC} to move failed files to",
                                     metavar='output')

    parser_schema_check.add_argument('-s', action='store_true', help=f"{cli_bcolors.OKBLUE}suppress{cli_bcolors.ENDC} verbose output", )

    parser_schema_check.set_defaults(func=check)

    #################### SCHEMA - GEN ############
    #   ___ ___ _  _
    #  / __| __| \| |
    # | (_ | _|| .` |
    #  \___|___|_|\_|

    parser_schema_gen = schema_subparsers.add_parser('gen',
                                                     help=f'Tool for {cli_bcolors.OKBLUE}generating{cli_bcolors.ENDC} schemas of YAML files',
                                                     description=f"""

            {cli_bcolors.HEADER}Tool for generating schemas of YAML files{cli_bcolors.ENDC}.
                """,
                                                     )

    parser_schema_gen.add_argument('-i', type=str, help=f"{cli_bcolors.OKBLUE}input file{cli_bcolors.ENDC}(s) to generate from",
                                   nargs='+', metavar='input')
    parser_schema_gen.add_argument('-o', type=str,
                                   help=f"{cli_bcolors.OKBLUE}output file{cli_bcolors.ENDC}(s) to write to",
                                   nargs='+', metavar='output')
    parser_schema_gen.add_argument('-d', type=str,
                                   help=f"{cli_bcolors.OKBLUE}directory{cli_bcolors.ENDC}(s) of files to generate from",
                                   default=None, nargs='+', metavar='dir')
    parser_schema_gen.add_argument('-t', type=str,
                            help=f"output {cli_bcolors.OKBLUE}type{cli_bcolors.ENDC} (JSON, YAML)",
                            default='yaml', metavar='type')
    parser_schema_gen.add_argument('-s', action='store_true',
                                   help=f"{cli_bcolors.OKBLUE}suppress{cli_bcolors.ENDC} verbose output", )

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