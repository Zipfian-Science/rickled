import importlib.util
import os
import sys
from io import StringIO

from rickled.tools import unparse_ini, CLIError, get_native_type_name
from rickled.tools import toml_null_stripper

from rickled import Rickle, UnsafeRickle
import re
import json
import yaml
import ast

import tomli_w as tomlw

def obj_get(args):
    dump_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()

            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)

            v = r.get(args.key)

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
    dump_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            r.set(args.key, args.value)

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
    dump_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            r.remove(args.key)

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
    output_type = args.OUTPUT_TYPE.strip().lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)
            v = r.get(args.key)

            try:
                print(get_native_type_name(python_type_name=type(v).__name__, format_type=output_type))
            except:
                raise CLIError(f"Unsupported output type {output_type}, try YAML, JSON, TOML, XML, or Python",
                               cli_tool=CLIError.CLITool.OBJ_GET)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.OBJ_TYPE)

def obj_search(args):
    dump_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = Rickle(_input, load_lambda=args.LOAD_LAMBDA)

            paths = r.search_path(args.key)

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

    dump_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
    try:
        re_pat = re.compile(r"(.+?)=(.+)")
        if args:
            if args.INPUT:
                _input = args.INPUT
            else:
                _input = sys.stdin.read()
            r = UnsafeRickle(_input, load_lambda=args.LOAD_LAMBDA)

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
