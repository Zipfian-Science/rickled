import importlib.util
import sys
from rickled.tools import cli_bcolors, CLIError
from rickled.tools import Schema
from rickled.tools import Converter
from rickled.tools import toml_null_stripper

import json
import yaml

import tomli_w as tomlw
def check(args):
    try:
        if args.INPUT:
            Schema(input_files=args.INPUT,
                   input_directories=[args.INPUT_DIRECTORY],
                   schema=args.SCHEMA,
                   output_dir=args.FAIL_DIRECTORY,
                   verbose=args.VERBOSE,
                   silent=args.SILENT,
                   use_json_schema=args.JSON_SCHEMA).do_validation()
        else:
            data = sys.stdin.read()
            input_data = Converter.infer_read_string_type(data)

            schema = Converter.infer_read_file_type(args.SCHEMA)

            passed = Schema.schema_validation(obj=input_data, schema=schema, no_print=not args.VERBOSE,
                                              use_json_schema=args.JSON_SCHEMA)

            if not args.SILENT:
                result = f"{cli_bcolors.OKGREEN}OK{cli_bcolors.ENDC}" if passed else f"{cli_bcolors.FAIL}FAIL{cli_bcolors.ENDC}"
                print(f"{cli_bcolors.OKBLUE}INPUT{cli_bcolors.ENDC} -> {result}")

            if not passed:
                sys.exit(1)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_CHECK)

def gen(args):
    output_type = args.OUTPUT_TYPE.lower().strip() if args.OUTPUT_TYPE else 'yaml'
    try:
        if args.INPUT:
            Schema(input_files=args.INPUT,
                   input_directories=[args.INPUT_DIRECTORY],
                   output_files=args.OUTPUT,
                   silent=args.SILENT,
                   default_output_type=output_type,
                   include_extended_properties=args.EXTRAS).do_generation()
        else:
            data = sys.stdin.read()
            input_data = Converter.infer_read_string_type(data)

            schema_dict = Schema.generate_schema_from_obj(input_data, include_extended_properties=args.EXTRAS)

            if output_type == 'yaml':
                print(yaml.dump(schema_dict))
            elif output_type == 'json':
                print(json.dumps(schema_dict))
            elif output_type == 'toml':
                print(tomlw.dumps(toml_null_stripper(schema_dict)))
            elif output_type == 'xml':
                if importlib.util.find_spec('xmltodict'):
                    import xmltodict
                    print(xmltodict.unparse({'schema':schema_dict}, pretty=True))
                else:
                    raise CLIError(message='Missing dependency "xmltodict" for type xml',
                                   cli_tool=CLIError.CLITool.SCHEMA_GEN)
            elif output_type == 'ini' or output_type == '.env':
                raise CLIError(message='INI and .ENV output unsupported for schema generation', cli_tool=CLIError.CLITool.SCHEMA_GEN)
            else:
                raise CLIError(message=f'Unknown type "{output_type}"', cli_tool=CLIError.CLITool.SCHEMA_GEN)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SCHEMA_GEN)
