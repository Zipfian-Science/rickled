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

from rickled import Rickle
import re
import json
import yaml
import ast

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
            if isinstance(v, Rickle):
                v = v.dict()
            elif v is None:
                v = ''

            if args.o:
                with open(args.o, 'w') as fp:
                    if args.t.lower() == 'json':
                        json.dump(v, fp)
                    else:
                        yaml.safe_dump(v, fp)
            else:
                if args.t.lower() == 'json':
                    print(json.dumps(v))
                else:
                    print(yaml.safe_dump(v))

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_GET)



def obj_set(args):
    try:
        if args:
            r = Rickle(args.i)
            r.set(args.key, args.value)

            if args.o:
                if args.t.lower() == 'json':
                    r.to_json_file(args.o)
                else:
                    r.to_yaml_file(args.o)
            else:
                if args.t.lower() == 'json':
                    print(r.to_json_string())
                else:
                    print(r.to_yaml_string())
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_SET)


def obj_del(args):
    try:
        if args:
            r = Rickle(args.i)
            r.remove(args.key)

            if args.o:
                if args.t.lower() == 'json':
                    r.to_json_file(args.o)
                else:
                    r.to_yaml_file(args.o)
            else:
                if args.t.lower() == 'json':
                    print(r.to_json_string())
                else:
                    print(r.to_yaml_string())
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
                    if args.t.lower() == 'json':
                        print(v.to_json_string())
                    else:
                        print(v.to_yaml_string())
                elif isinstance(v, dict):
                    if args.t.lower() == 'json':
                        print(json.dumps(v))
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
        rick = Rickle(args.f)

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
                               interface=args.a
                               )
        else:
            serve_rickle_http(rickle=rick,
                              port=args.p,
                              interface=args.a
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
-----------------------------------------------------
{cli_bcolors.HEADER}YAML tools for Python{cli_bcolors.ENDC} (version {ver}).
""",
        epilog="-----------------------------------------------------"
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
                                        help=f'Tool for {cli_bcolors.OKBLUE}converting{cli_bcolors.ENDC} files to or from YAML',
                                        description=f"""
---
{cli_bcolors.HEADER}Tool for converting files to or from YAML{cli_bcolors.ENDC}.
    """,
                                        epilog="-----------------------------------------------------"
                                        )

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
    ---
    {cli_bcolors.HEADER}Tool for accessing/manipulating YAML files{cli_bcolors.ENDC}.
        """,
                                       epilog="-----------------------------------------------------"
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
                                               help=f'Tool for {cli_bcolors.OKBLUE}getting{cli_bcolors.ENDC} values from YAML files',
                                               description=f"""
        ---
        {cli_bcolors.HEADER}Tool for getting values from YAML files{cli_bcolors.ENDC}.
            """,
                                               epilog="-----------------------------------------------------"
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
                                               help=f'Tool for {cli_bcolors.OKBLUE}setting{cli_bcolors.ENDC} values in YAML files',
                                               description=f"""
            ---
            {cli_bcolors.HEADER}Tool for setting values in YAML files{cli_bcolors.ENDC}.
                """,
                                               epilog="-----------------------------------------------------"
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
                                               help=f'Tool for {cli_bcolors.OKBLUE}deleting{cli_bcolors.ENDC} keys in YAML files',
                                               description=f"""
                ---
                {cli_bcolors.HEADER}Tool for deleting keys in YAML files{cli_bcolors.ENDC}.
                    """,
                                               epilog="-----------------------------------------------------"
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
                                                help=f'Tool for {cli_bcolors.OKBLUE}checking type{cli_bcolors.ENDC} of keys in YAML files',
                                                description=f"""
                    ---
                    {cli_bcolors.HEADER}Tool for checking type of keys in YAML files{cli_bcolors.ENDC}.
                        """,
                                                epilog="-----------------------------------------------------"
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
                                                  help=f'Tool for {cli_bcolors.OKBLUE}searching{cli_bcolors.ENDC} keys in YAML files',
                                                  description=f"""
                    ---
                    {cli_bcolors.HEADER}Tool for searching keys in YAML files{cli_bcolors.ENDC}.
                        """,
                                                  epilog="-----------------------------------------------------"
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
                                                help=f'Tool for {cli_bcolors.OKBLUE}executing function{cli_bcolors.ENDC} defined in YAML files',
                                                description=f"""
                    ---
                    {cli_bcolors.HEADER}Tool for executing function defined in YAML files{cli_bcolors.ENDC}.
                        """,
                                                epilog="-----------------------------------------------------"
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
                                         help=f'Tool for serving YAML via {cli_bcolors.OKBLUE}http(s){cli_bcolors.ENDC}',
                                         description=f"""
    ---
    {cli_bcolors.HEADER}Tool for serving YAML via http(s){cli_bcolors.ENDC}.
        """,
                                         epilog="-----------------------------------------------------"
                                         )

    parser_serve.add_argument('-f', type=str,
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
    parser_serve.set_defaults(func=serve)

    #################### SCHEMA #####################
    # ░░      ░░░      ░░  ░░░░  ░        ░  ░░░░  ░░      ░░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒   ▒▒   ▒  ▒▒▒▒  ▒
    # ▓▓      ▓▓  ▓▓▓▓▓▓▓        ▓      ▓▓▓        ▓  ▓▓▓▓  ▓
    # ███████  █  ████  █  ████  █  ███████  █  █  █        █
    # ██      ███      ██  ████  █        █  ████  █  ████  █


    parser_schema = subparsers.add_parser('schema',
                                          help=f'Tool for generating and checking {cli_bcolors.OKBLUE}schemas{cli_bcolors.ENDC} of YAML files',
                                          description=f"""
    ---
    {cli_bcolors.HEADER}Tool for generating and checking schemas of YAML files{cli_bcolors.ENDC}.
        """,
                                          epilog="-----------------------------------------------------"
                                          )

    schema_subparsers = parser_schema.add_subparsers()

    #################### SCHEMA - CHECK ############
    #   ___ _  _ ___ ___ _  __
    #  / __| || | __/ __| |/ /
    # | (__| __ | _| (__| ' <
    #  \___|_||_|___\___|_|\_\

    parser_schema_check = schema_subparsers.add_parser('check',
                                                       help=f'Tool for {cli_bcolors.OKBLUE}checking{cli_bcolors.ENDC} schemas of YAML files',
                                                       description=f"""
        ---
        {cli_bcolors.HEADER}Tool for checking schemas of YAML files{cli_bcolors.ENDC}.
            """,
                                                       epilog="-----------------------------------------------------"
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
            ---
            {cli_bcolors.HEADER}Tool for generating schemas of YAML files{cli_bcolors.ENDC}.
                """,
                                                     epilog="-----------------------------------------------------"
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
    except AttributeError as exc:
        sys.stderr.write(f'\n{cli_bcolors.FAIL}error: {exc}{cli_bcolors.ENDC}\n\n')
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
            parser_conv.print_help(sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()