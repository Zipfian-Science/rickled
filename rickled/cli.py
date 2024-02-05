# ASCCI Text found in this file was generated on
# https://patorjk.com/software/taag/
# Large heading using "Shaded Blocky" font
# Sub headings using "Small" font

import rickled.__version__ as ver
import argparse
from rickled.tools import bcolors
from rickled.tools import Schema
from rickled.tools import Converter
from rickled.net import serve_rickle_http, serve_rickle_https
from rickled import Rickle
import re
import json
import yaml
import ast


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def conv(args):
    Converter(input_files=args.i,
              output_files=args.o,
              input_directories=args.d,
              default_output_type=args.t,
              silent=args.s).do_convert()

def obj_get(args):
    import json
    import yaml
    if args:
        r = Rickle(args.i, load_lambda=args.l)
        v = r.get(args.key)
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



def obj_set(args):
    if args:
        r = Rickle(args.i)
        r.set(args.key, args.value)
        if args.p:
            if args.t.lower() == 'json':
                print(r.to_json_string())
            else:
                print(r.to_yaml_string())
        if args.o:
            if args.t.lower() == 'json':
                r.to_json_file(args.o)
            else:
                r.to_yaml_file(args.o)


def obj_del(args):
    if args:
        r = Rickle(args.i)
        r.remove(args.key)
        if args.p:
            if args.t.lower() == 'json':
                print(r.to_json_string())
            else:
                print(r.to_yaml_string())
        if args.o:
            if args.t.lower() == 'json':
                r.to_json_file(args.o)
            else:
                r.to_yaml_file(args.o)

def obj_type(args):
    if args:
        r = Rickle(args.i, load_lambda=args.l)
        v = r.get(args.key)
        print(type(v))

def obj_search(args):
    if args:
        r = Rickle(args.i, load_lambda=args.l)
        paths = r.search_path(args.key)
        for p in paths:
            print(p)

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


def serve(args):
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

def check(args):
    Schema(input_files=args.i,
           input_directories=args.d,
           schema=args.c,
           output_dir=args.o,
           silent=args.s).do_validation()

def gen(args):
    Schema(input_files=args.i,
           input_directories=args.d,
           silent=args.s).do_generation()

def main():
    parser = argparse.ArgumentParser(
        prog='rickle',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"""
-----------------------------------------------------
{bcolors.HEADER}YAML tools for Python{bcolors.ENDC} (version {ver}).
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
                                        help=f'Tool for {bcolors.OKBLUE}converting{bcolors.ENDC} files to or from YAML',
                                        description=f"""
---
{bcolors.HEADER}Tool for converting files to or from YAML{bcolors.ENDC}.
    """,
                                        epilog="-----------------------------------------------------"
                                        )

    parser_conv.add_argument('-i', type=str, help=f"{bcolors.OKBLUE}input file{bcolors.ENDC}(s) to convert",
                             nargs='+', metavar='input')
    parser_conv.add_argument('-d', type=str, help=f"{bcolors.OKBLUE}directory{bcolors.ENDC}(s) of input files",
                             default=None, nargs='+', metavar='dir')
    parser_conv.add_argument('-o', type=str, help=f"{bcolors.OKBLUE}output file{bcolors.ENDC} names",
                             nargs='+', metavar='output')
    parser_conv.add_argument('-t', type=str, help=f"default output {bcolors.OKBLUE}file type{bcolors.ENDC} (JSON, YAML)",
                             default='yaml', metavar='type')
    parser_conv.add_argument('-s', action='store_true', help=f"{bcolors.OKBLUE}suppress{bcolors.ENDC} verbose output",)

    parser_conv.set_defaults(func=conv)

    #################### OBJ #####################
    # ░░      ░░       ░░        ░
    # ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒▒▒▒▒▒  ▒
    # ▓  ▓▓▓▓  ▓       ▓▓▓▓▓▓▓▓  ▓
    # █  ████  █  ████  █  ████  █
    # ██      ██       ███      ██


    parser_obj = subparsers.add_parser('obj',
                                        help=f'Tool for {bcolors.OKBLUE}accessing/manipulating{bcolors.ENDC} YAML files',
                                        description=f"""
    ---
    {bcolors.HEADER}Tool for accessing/manipulating YAML files{bcolors.ENDC}.
        """,
                                        epilog="-----------------------------------------------------"
                                        )

    parser_obj.add_argument('-i', type=str, help=f"{bcolors.OKBLUE}input file{bcolors.ENDC} to read/modify",
                            metavar='input', required=True)
    parser_obj.add_argument('-o', type=str, help=f"{bcolors.OKBLUE}output file{bcolors.ENDC} to save modified",
                            metavar='output', required=False)
    parser_obj.add_argument('-t', type=str,
                             help=f"output {bcolors.OKBLUE}type{bcolors.ENDC} (JSON, YAML)",
                             default='yaml', metavar='type')
    parser_obj.add_argument('-p', action='store_true', help=f"{bcolors.OKBLUE}print{bcolors.ENDC} output",
                            default=False)
    parser_obj.add_argument('-l', action='store_true', help=f"load {bcolors.OKBLUE}lambda{bcolors.ENDC} types",
                            default=False)

    subparsers_obj = parser_obj.add_subparsers()

    #################### OBJ - GET #####################
    #   ___ ___ _____
    #  / __| __|_   _|
    # | (_ | _|  | |
    #  \___|___| |_|

    get_obj_parser = subparsers_obj.add_parser('get',
                       help=f'Tool for {bcolors.OKBLUE}getting{bcolors.ENDC} values from YAML files',
                       description=f"""
        ---
        {bcolors.HEADER}Tool for getting values from YAML files{bcolors.ENDC}.
            """,
                                          epilog="-----------------------------------------------------"
                                          )

    get_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} to get value",
                            metavar='key')

    get_obj_parser.set_defaults(func=obj_get)

    #################### OBJ - SET #####################
    #  ___ ___ _____
    # / __| __|_   _|
    # \__ \ _|  | |
    # |___/___| |_|

    set_obj_parser = subparsers_obj.add_parser('set',
                                               help=f'Tool for {bcolors.OKBLUE}setting{bcolors.ENDC} values in YAML files',
                                               description=f"""
            ---
            {bcolors.HEADER}Tool for setting values in YAML files{bcolors.ENDC}.
                """,
                                               epilog="-----------------------------------------------------"
                                               )

    set_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} to set value",
                                metavar='key')
    set_obj_parser.add_argument('value', type=str, help=f"{bcolors.OKBLUE}Value{bcolors.ENDC} to set",
                                metavar='value')

    set_obj_parser.set_defaults(func=obj_set)

    #################### OBJ - DEL #####################
    #  ___  ___ _
    # |   \| __| |
    # | |) | _|| |__
    # |___/|___|____|

    del_obj_parser = subparsers_obj.add_parser('del',
                                               help=f'Tool for {bcolors.OKBLUE}deleting{bcolors.ENDC} keys in YAML files',
                                               description=f"""
                ---
                {bcolors.HEADER}Tool for deleting keys in YAML files{bcolors.ENDC}.
                    """,
                                               epilog="-----------------------------------------------------"
                                               )

    del_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} to delete",
                                metavar='key')

    del_obj_parser.set_defaults(func=obj_del)

    #################### OBJ - TYPE #####################
    #  _______   _____ ___
    # |_   _\ \ / / _ \ __|
    #   | |  \ V /|  _/ _|
    #   |_|   |_| |_| |___|

    type_obj_parser = subparsers_obj.add_parser('type',
                                               help=f'Tool for {bcolors.OKBLUE}checking type{bcolors.ENDC} of keys in YAML files',
                                               description=f"""
                    ---
                    {bcolors.HEADER}Tool for checking type of keys in YAML files{bcolors.ENDC}.
                        """,
                                               epilog="-----------------------------------------------------"
                                               )

    type_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} to check",
                                metavar='key')

    type_obj_parser.set_defaults(func=obj_type)

    #################### OBJ - SEARCH #####################
    #  ___ ___   _   ___  ___ _  _
    # / __| __| /_\ | _ \/ __| || |
    # \__ \ _| / _ \|   / (__| __ |
    # |___/___/_/ \_\_|_\\___|_||_|

    search_obj_parser = subparsers_obj.add_parser('search',
                                               help=f'Tool for {bcolors.OKBLUE}searching{bcolors.ENDC} keys in YAML files',
                                               description=f"""
                    ---
                    {bcolors.HEADER}Tool for searching keys in YAML files{bcolors.ENDC}.
                        """,
                                               epilog="-----------------------------------------------------"
                                               )

    search_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} to search",
                                metavar='key')

    search_obj_parser.set_defaults(func=obj_search)

    #################### OBJ - FUNC #####################
    #  ___ _   _ _  _  ___
    # | __| | | | \| |/ __|
    # | _|| |_| | .` | (__
    # |_|  \___/|_|\_|\___|

    func_obj_parser = subparsers_obj.add_parser('func',
                                               help=f'Tool for {bcolors.OKBLUE}executing function{bcolors.ENDC} defined in YAML files',
                                               description=f"""
                    ---
                    {bcolors.HEADER}Tool for executing function defined in YAML files{bcolors.ENDC}.
                        """,
                                               epilog="-----------------------------------------------------"
                                               )

    func_obj_parser.add_argument('-x', action='store_true', help=f"{bcolors.OKBLUE}infer parameter{bcolors.ENDC} types",
                            default=False)
    func_obj_parser.add_argument('key', type=str, help=f"{bcolors.OKBLUE}Key{bcolors.ENDC} (name) of function",
                                metavar='key')
    func_obj_parser.add_argument('params', type=str, help=f"{bcolors.OKBLUE}Params{bcolors.ENDC} for function",
                                 metavar='params', nargs='+')

    func_obj_parser.set_defaults(func=obj_func)


    #################### SERVE #####################
    # ░░      ░░        ░       ░░  ░░░░  ░        ░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒
    # ▓▓      ▓▓      ▓▓▓       ▓▓▓  ▓▓  ▓▓      ▓▓▓
    # ███████  █  ███████  ███  ████    ███  ███████
    # ██      ██        █  ████  ████  ████        █


    parser_serve = subparsers.add_parser('serve',
                                        help=f'Tool for serving YAML via {bcolors.OKBLUE}http(s){bcolors.ENDC}',
                                        description=f"""
    ---
    {bcolors.HEADER}Tool for serving YAML via http(s){bcolors.ENDC}.
        """,
                                        epilog="-----------------------------------------------------"
                                        )

    parser_serve.add_argument('-f', type=str,
                              help=f"{bcolors.OKBLUE}YAML{bcolors.ENDC} or {bcolors.OKBLUE}JSON{bcolors.ENDC} file to serve",
                              metavar='file')
    # TODO implement config
    # parser_serve.add_argument('-c', type=str, help=f"{bcolors.OKBLUE}config{bcolors.ENDC} file path",
    #                           default=None, metavar='config')
    parser_serve.add_argument('-a', type=str, help=f"{bcolors.OKBLUE}host address{bcolors.ENDC}",
                              default='', metavar='address')
    parser_serve.add_argument('-p', type=int, help=f"{bcolors.OKBLUE}port{bcolors.ENDC} number",
                              default=8080, metavar='port')
    parser_serve.add_argument('-k', type=str, help=f"{bcolors.OKBLUE}private key{bcolors.ENDC} file path",
                              default=None, metavar='privkey')
    parser_serve.add_argument('-c', type=str, help=f"{bcolors.OKBLUE}SSL certificate{bcolors.ENDC} file path",
                              default=None, metavar='cert')
    parser_serve.add_argument('-b', action='store_true', help=f"open URL in {bcolors.OKBLUE}browser{bcolors.ENDC}", )
    parser_serve.set_defaults(func=serve)

    #################### SCHEMA #####################
    # ░░      ░░░      ░░  ░░░░  ░        ░  ░░░░  ░░      ░░
    # ▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒   ▒▒   ▒  ▒▒▒▒  ▒
    # ▓▓      ▓▓  ▓▓▓▓▓▓▓        ▓      ▓▓▓        ▓  ▓▓▓▓  ▓
    # ███████  █  ████  █  ████  █  ███████  █  █  █        █
    # ██      ███      ██  ████  █        █  ████  █  ████  █


    parser_schema = subparsers.add_parser('schema',
                                        help=f'Tool for generating and checking {bcolors.OKBLUE}schemas{bcolors.ENDC} of YAML files',
                                        description=f"""
    ---
    {bcolors.HEADER}Tool for generating and checking schemas of YAML files{bcolors.ENDC}.
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
                                          help=f'Tool for {bcolors.OKBLUE}checking{bcolors.ENDC} schemas of YAML files',
                                          description=f"""
        ---
        {bcolors.HEADER}Tool for checking schemas of YAML files{bcolors.ENDC}.
            """,
                                          epilog="-----------------------------------------------------"
                                          )


    parser_schema_check.add_argument('-i', type=str, help=f"{bcolors.OKBLUE}input file{bcolors.ENDC}(s) to check",
                             nargs='+', metavar='input')
    parser_schema_check.add_argument('-d', type=str, help=f"{bcolors.OKBLUE}directory{bcolors.ENDC}(s) of files to check",
                             default=None, nargs='+', metavar='dir')

    parser_schema_check.add_argument('-c', type=str, help=f"{bcolors.OKBLUE}schema definition file{bcolors.ENDC} to compare",
                                     metavar='schema')

    parser_schema_check.add_argument('-o', type=str,
                                     help=f"{bcolors.OKBLUE}output directory{bcolors.ENDC} to move failed files to",
                                     metavar='output')

    parser_schema_check.add_argument('-s', action='store_true', help=f"{bcolors.OKBLUE}suppress{bcolors.ENDC} verbose output", )

    parser_schema_check.set_defaults(func=check)

    #################### SCHEMA - GEN ############
    #   ___ ___ _  _
    #  / __| __| \| |
    # | (_ | _|| .` |
    #  \___|___|_|\_|

    parser_schema_gen = schema_subparsers.add_parser('gen',
                                                       help=f'Tool for {bcolors.OKBLUE}generating{bcolors.ENDC} schemas of YAML files',
                                                       description=f"""
            ---
            {bcolors.HEADER}Tool for generating schemas of YAML files{bcolors.ENDC}.
                """,
                                                       epilog="-----------------------------------------------------"
                                                       )

    parser_schema_gen.add_argument('-i', type=str, help=f"{bcolors.OKBLUE}input file{bcolors.ENDC}(s) to generate from",
                                     nargs='+', metavar='input')
    parser_schema_gen.add_argument('-d', type=str,
                                     help=f"{bcolors.OKBLUE}directory{bcolors.ENDC}(s) of files to generate from",
                                     default=None, nargs='+', metavar='dir')

    parser_schema_gen.add_argument('-s', action='store_true',
                                     help=f"{bcolors.OKBLUE}suppress{bcolors.ENDC} verbose output", )

    parser_schema_gen.set_defaults(func=gen)

    #################################################

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()