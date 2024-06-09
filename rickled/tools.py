import configparser
import importlib.util
from typing import List, Union
from pathlib import Path
import yaml
import json
import os
import sys
import re
from collections import OrderedDict, namedtuple, defaultdict

import tomli_w as tomlw
if sys.version_info < (3, 11):
    import tomli as toml
else:
    import tomllib as toml

def toml_null_stripper(dictionary: dict) -> dict:
    """
    Remove null valued key-value pairs.

    Args:
        dictionary (dict): Input dictionary.

    Returns:
        dict: Output dictionary.
    """
    new_dict = {}
    for k, v in dictionary.items():
        if isinstance(v, dict):
            v = toml_null_stripper(v)
        if v not in (u"", None, {}):
            new_dict[k] = v
    return new_dict


def parse_ini(config: configparser.ConfigParser, path_sep: str = None, list_brackets: tuple = None):
    """
    Func to create a dictionary from an initialised config parser and then returns inflated dictionary.

    Args:
        config (ConfigParser): Initialised ConfigParser.
        path_sep (str): For inflating sections from deeply nested structures (default = None).
        list_brackets (tuple): For list indexes, type of bracket (default = None).

    Returns:
        dict:
    """
    _d = {section_name: dict(config[section_name]) for section_name in config.sections()}

    if path_sep is None:
        path_sep = os.getenv("RICKLE_INI_PATH_SEP", ".")

    if list_brackets is None:
        list_brackets = (os.getenv("RICKLE_INI_OPENING_BRACES", "("),
                                                os.getenv("RICKLE_INI_CLOSING_BRACES", ")"))

    __d = dict()
    for k, v in _d.items():
        for kk, vv in v.items():
            __d[f"{k}{path_sep}{kk}"] = vv

    _d = inflate_dict(flat_dict=__d, path_sep=path_sep, list_brackets=list_brackets)
    return _d

def unparse_ini(dictionary: dict, path_sep: str = None, list_brackets: tuple = None) -> configparser.ConfigParser:
    """
    Function to flatten a dictionary and create ConfigParser from the result.

    Args:
        dictionary (dict): Any dictionary.
        path_sep (str): For creating sections from deeply nested structures (default = None).
        list_brackets (tuple): For list indexes, type of bracket (default = None).

    Returns:
        ConfigParser: Config parser with flattened dictionary set.
    """
    flattened_dict = flatten_dict(dictionary=dictionary, path_sep=path_sep, list_brackets=list_brackets)

    ini_dict = defaultdict(dict)
    for k, v in flattened_dict.items():
        splits = k.split(path_sep)
        sect = path_sep.join(splits[:-1])
        sect = path_sep if sect == '' else sect
        ini_dict[sect][splits[-1]] = v

    output_ini = configparser.ConfigParser()
    output_ini.read_dict(ini_dict)

    return output_ini

def flatten_dict(dictionary, path_sep: str = None, list_brackets: tuple = ('(', ')')):
    """
    Flattens a deepl structure python dictionary into a shallow (or 'thin') dictionary of depth 1.

    Notes:
        Dictionary can only contain types str, bool, int, float, dict, list. Any other types won't be expanded upon.

    Args:
        dictionary (dict): Input dictionary.
        path_sep (str): Path separator.
        list_brackets (tuple): Tuple of strings for list index values (default = ('(', ')')).

    Returns:
        dict: Flattened to depth 1.
    """
    def __flatten_dict(d, parent_path: str = None, sep: str = None):

        values = list()
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, dict):
                    value = __flatten_dict(d=v, parent_path=f'{parent_path}{sep}{k}', sep=sep)
                    values.extend(value)
                elif isinstance(v, list):
                    value = __flatten_dict(d=v, parent_path=f'{parent_path}{sep}{k}', sep=sep)
                    values.extend(value)
                else:
                    values.append({f'{parent_path}{sep}{k}': v})
        if isinstance(d, list):
            for i, val in enumerate(d):
                if isinstance(val, dict):
                    value = __flatten_dict(d=val, parent_path=f'{parent_path}{sep}{list_brackets[0]}{i}{list_brackets[1]}', sep=sep)
                    values.extend(value)
                elif isinstance(val, list):
                    value = __flatten_dict(d=val, parent_path=f'{parent_path}{sep}{list_brackets[0]}{i}{list_brackets[1]}', sep=sep)
                    values.extend(value)
                else:
                    values.append({f'{parent_path}{sep}{list_brackets[0]}{i}{list_brackets[1]}': val})
        return values

    list_dicts = __flatten_dict(d=dictionary, parent_path='', sep=path_sep)
    flattened_dict = dict()
    for d in list_dicts:
        for k, v in d.items():
            flattened_dict[k.lstrip(path_sep)] = v
    return flattened_dict


def inflate_dict(flat_dict: dict, path_sep: str = None, list_brackets: tuple = ('(', ')')):
    """
    Does reverse operation of ``flatten_dict`` and inflates a shallow dictionary.

    Args:
        flat_dict (dict): Input dictionary, can be any dict (won't have an effect).
        path_sep (str): Path separator.
        list_brackets (tuple): Tuple of strings for list index values (default = ('(', ')')).

    Returns:
        dict: Inflated dictionary.
    """
    Node = namedtuple('Node', ['key', 'struc_type'])

    def unravel(key, path_sep: str = None, list_brackets: tuple = ('(', ')')):

        if key.startswith(path_sep):
            key = key[1:]
        keys = key.split(path_sep)

        _list = list()
        for k in keys:
            pat = f'\\{list_brackets[0]}(\\d+)\\{list_brackets[1]}'

            m = re.match(pat, k)
            if m:
                _list.append(Node(key=int(m.group(1)), struc_type='list'))
            else:
                _list.append(Node(key=k, struc_type='dict'))

        return _list

    main_d = dict()
    lists = dict()
    dicts = dict()

    for key, value in flat_dict.items():
        d = main_d

        keys = unravel(key, path_sep=path_sep, list_brackets=list_brackets)

        for i, k in enumerate(keys[:-1]):
            if k.struc_type == 'dict':
                if k.key not in d:
                    d[k.key] = list() if keys[i + 1].struc_type == 'list' else dict()
                d = d[k.key]
            if k.struc_type == 'list':

                f = '/'.join([str(p.key) for p in keys[:i + 1]])
                if f in lists:
                    _ = lists[f]
                elif f in dicts:
                    _ = dicts[f]
                else:
                    _ = list() if keys[i + 1].struc_type == 'list' else dict()
                    if isinstance(_, list):
                        lists[f] = _
                    else:
                        dicts[f] = _
                    d.insert(k.key, _)
                d = _

        if isinstance(d, dict):
            d[keys[-1].key] = value
        if isinstance(d, list):
            d.insert(keys[-1].key, value)

    return main_d


class cli_bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Schema:
    """
    Tool for inferring schemas from Python dicts and validating schemas.

    Args:
        input_files (list): List of input file paths (default = None).
        input_directories (list): List of directories (default = None).
        schema (str, dict): The dict definition of schema or path to schema file (default = None).
        output_dir (str): Directory to move output files to (default = None).
        silent (bool): Suppress verbose output (default = None).
    """

    supported_list = f"{cli_bcolors.OKBLUE}YAML (r/w), JSON (r/w), TOML (r/w), XML (r){cli_bcolors.ENDC}"

    def __init__(self,
                 input_files: List[str] = None,
                 input_directories: List[str] = None,
                 schema: Union[str, dict] = None,
                 output_files: List[str] = None,
                 output_dir: str = None,
                 silent: bool = False,
                 default_output_type: str = 'yaml'
                 ):
        self.input_files = input_files
        self.input_directories = input_directories

        if isinstance(schema, str):
            self.schema = Converter.infer_read_file_type(schema)
        else:
            self.schema = schema

        self.output_files = output_files

        self.output_dir = output_dir

        self.silent = silent
        if default_output_type.strip().lower() == 'yml':
            default_output_type = 'yaml'
        self.default_output_type = default_output_type.strip().lower()

    def do_generation(self):
        """
        Generates schema files for the given input files.
        """
        if self.input_files is None and self.input_directories is None:
            raise ValueError("Either input_files or input_directories must be defined!")

        if self.input_files is None and not self.input_directories is None:
            self.input_files = list()
            for d in self.input_directories:
                dir_path = Path(d)
                self.input_files.extend(list(dir_path.glob("*.yaml")))
                self.input_files.extend(list(dir_path.glob("*.yml")))
                self.input_files.extend(list(dir_path.glob("*.json")))
                self.input_files.extend(list(dir_path.glob("*.toml")))
                self.input_files.extend(list(dir_path.glob("*.xml")))

        if self.output_files is None:
            self.output_files = list()
            out_dir = f"{self.output_dir}/" if self.output_dir else './'
            for input_file in self.input_files:
                self.output_files.append(f"{out_dir}{os.path.splitext(input_file)[0]}.schema.{self.default_output_type.lower()}")


        zipped = zip(self.input_files, self.output_files)

        for pair in zipped:
            try:
                input_data = Converter.infer_read_file_type(pair[0])
                output_file = Path(pair[1])

                suffix = output_file.suffix.lower() if output_file.suffix else f".{self.default_output_type}"

                schema = Schema.generate_schema_from_obj(input_data)

                if suffix == '.yaml':
                    with output_file.open("w") as fout:
                        yaml.safe_dump(schema, fout)

                if suffix == '.json':
                    with output_file.open("w") as fout:
                        json.dump(schema, fout)

                if suffix == '.toml':
                    with output_file.open("wb") as fout:
                        tomlw.dump(toml_null_stripper(schema), fout)

                if suffix == '.xml':
                    if importlib.util.find_spec('xmltodict'):
                        import xmltodict

                        with output_file.open("wb") as fin:
                            return xmltodict.unparse(schema,fin)

                if not self.silent:
                    print(f"{cli_bcolors.OKBLUE}{pair[0]}{cli_bcolors.ENDC} -> {cli_bcolors.OKBLUE}{pair[1]}{cli_bcolors.ENDC}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{cli_bcolors.FAIL}{str(exc)}{cli_bcolors.ENDC}")
                continue
    def do_validation(self):
        """
        Validates input files against schema definition.

        Returns:
            list: List of files that did not pass validation.
        """
        failed_validation = list()

        if self.input_files is None and self.input_directories is None:
            raise ValueError("Either input_files or input_directories must be defined!")

        if self.input_files is None and not self.input_directories is None:
            self.input_files = list()
            for d in self.input_directories:
                dir_path = Path(d)
                self.input_files.extend(list(dir_path.glob("*.yaml")))
                self.input_files.extend(list(dir_path.glob("*.yml")))
                self.input_files.extend(list(dir_path.glob("*.json")))
                self.input_files.extend(list(dir_path.glob("*.toml")))
                self.input_files.extend(list(dir_path.glob("*.xml")))

        for file in self.input_files:
            try:
                input_data = Converter.infer_read_file_type(file)

                passed = Schema.schema_validation(input_data, self.schema, no_print=self.silent)

                if not passed:
                    failed_validation.append(file)

                if not self.silent:
                    result = f"{cli_bcolors.OKGREEN}OK{cli_bcolors.ENDC}" if passed else f"{cli_bcolors.FAIL}FAIL{cli_bcolors.ENDC}"
                    print(f"{cli_bcolors.OKBLUE}{file}{cli_bcolors.ENDC} -> {result}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{cli_bcolors.FAIL}{str(exc)}{cli_bcolors.ENDC}")
                continue

        if self.output_dir:
            outdir = Path(self.output_dir)
            if not outdir.is_dir():
                outdir.mkdir()

            for f in failed_validation:
                f_path = Path(f)
                f_path.rename(outdir / f_path.name)


        return failed_validation

    @staticmethod
    def _extract_data_types(value: Union[list, dict, str, int, float, bool]):
        if isinstance(value, list):
            schema = list()
            for v in value:
                schema.append(Schema._extract_data_types(v))
            return schema
        if isinstance(value, dict):
            schema = OrderedDict()
            for k, v in value.items():
                schema[k] = Schema._extract_data_types(v)
            return schema
        if isinstance(value, str):
            return str
        if isinstance(value, int):
            return int
        if isinstance(value, float):
            return float
        if isinstance(value, bool):
            return bool

    @staticmethod
    def _data_types_to_schema(value: Union[list, dict, str, int, float, bool, None]):

        if value == bool:
            return {'type': 'bool'}
        if value == str:
            return {'type': 'str'}
        if value == int:
            return {'type': 'int'}
        if value == float:
            return {'type': 'float'}
        if value is None:
            return {'type': 'any'}

        if isinstance(value, dict):
            named_schema = OrderedDict()
            named_schema['type'] = 'dict'
            named_schema['schema'] = OrderedDict()
            for k, v in value.items():
                named_schema['schema'][k] = Schema._data_types_to_schema(v)
            return named_schema

        if isinstance(value, list):
            named_schema = OrderedDict()
            named_schema['type'] = 'list'
            named_schema['schema'] = list()
            list_data_types = set(value)

            if len(list_data_types) > 1:
                named_schema['schema'].append(Schema._data_types_to_schema(None))
            if len(list_data_types) == 1:
                named_schema['schema'].append(Schema._data_types_to_schema(list_data_types.pop()))
            return named_schema

    @staticmethod
    def generate_schema_from_obj(obj):
        """
        Generate a schema definition from a Python object.

        Args:
            obj: Dict like object.

        Returns:
            dict: Schema detected from obj.

        """
        rep = Schema._extract_data_types(obj)
        return Schema._data_types_to_schema(rep)

    @staticmethod
    def schema_validation(obj, schema: dict, path: str = '', no_print: bool = False) -> bool:
        """
        Validates if obj conforms to schema.

        Args:
            obj: The object to check.
            schema (dict): The schema in dict form.
            path (str): The current path of the object tree (default = 'root').
            no_print (bool): If failures should not be printed (default = False).

        Returns:
            bool: True if the object conforms.
        """
        new_path = path
        if schema['type'] == 'dict':
            for k, v in schema['schema'].items():
                new_path = f"{new_path}/{k}"
                req = v.get('required', False)
                nullable = v.get('nullable', False)
                present = k in obj.keys()
                if not present:
                    if req:
                        if not no_print:
                            print(f"Required {cli_bcolors.FAIL}'{k}'{cli_bcolors.ENDC} (per schema {v}),\n In {obj},\n Path {cli_bcolors.WARNING}{new_path}{cli_bcolors.ENDC}")
                        return False
                    else:
                        new_path = path
                        continue

                null_no_type = nullable & ((v['type'] == 'any') | (type(obj[k]).__name__ == 'NoneType'))
                null_with_type = nullable & (v['type'] != 'any') & (type(obj[k]).__name__ == v['type'])
                non_null = (nullable is False) & ((v['type'] == 'any') | (type(obj[k]).__name__ == v['type']))

                if not (null_no_type or null_with_type or non_null):
                    if not no_print:
                        print(
                        f"Type '{k}' == {cli_bcolors.FAIL}'{type(obj[k]).__name__}'{cli_bcolors.ENDC},\n Required type {cli_bcolors.OKBLUE}'{v['type']}'{cli_bcolors.ENDC} (per schema {v}),\n In {obj},\n Path {cli_bcolors.WARNING}{new_path}{cli_bcolors.ENDC}")
                    return False

                if v['type'] in ['dict', 'list']:
                    if not Schema.schema_validation(obj[k], v, path=new_path, no_print=no_print):
                        return False
                new_path = path
            return True
        if schema['type'] == 'list':

            nullable = schema.get('nullable', False)

            if nullable and obj is None:
                return True

            length = schema.get('length', -1)
            obj_length = len(obj)
            schema_len = len(schema['schema'])

            if length > -1 and obj_length != length:
                if not no_print:
                    print(
                    f"Length '{obj}' == {cli_bcolors.FAIL}{obj_length}{cli_bcolors.ENDC},\n Required length {cli_bcolors.OKBLUE}{length}{cli_bcolors.ENDC} (per schema {schema['schema']}),\n In {obj},\n Path {cli_bcolors.WARNING}{new_path}{cli_bcolors.ENDC}")
                return False

            if schema_len > 0:
                single_type = schema['schema'][0]

                for i in range(obj_length):
                    new_path = f"{new_path}/[{i}]"
                    o = obj[i]
                    if single_type['type'] != 'any' and type(o).__name__ != single_type['type']:
                        if not no_print:
                            print(
                            f"Type '{o}' == {cli_bcolors.FAIL}'{type(o).__name__}'{cli_bcolors.ENDC},\n Required type {cli_bcolors.OKBLUE}'{single_type['type']}'{cli_bcolors.ENDC} (per schema {single_type}),\n In {o},\n Path {cli_bcolors.WARNING}{new_path}{cli_bcolors.ENDC}")
                        return False
                    if single_type['type'] in ['dict', 'list']:
                        if not Schema.schema_validation(o, single_type, path=new_path, no_print=no_print):
                            return False
                    new_path = path
            return True

class Converter:
    """
    Tool for converting between YAML and JSON (and TOML, XML, INI, .ENV), mainly to be used in CLI.

    Args:
        input_files (list): List of input file paths (default = None).
        input_directories (list): List of directories (default = None).
        output_files (list): List of output file paths (default = None).
        default_output_type (str): Default type to convert to if output files are not provided (default = 'yaml').
        silent (bool): Suppress verbose output (default = None).
    """

    supported_list = f"{cli_bcolors.OKBLUE}YAML (r/w), JSON (r/w), TOML (r/w), INI (r/w), XML (r/w), .ENV (r){cli_bcolors.ENDC}"

    def __init__(self,
                 input_files: List[str] = None,
                 input_directories: List[str] = None,
                 output_files: List[str] = None,
                 default_output_type: str = 'yaml',
                 silent: bool = False,
                 ):
        self.input_files = input_files
        self.input_directories = input_directories
        self.output_files = output_files
        self.default_output_type = default_output_type
        self.silent = silent
        if importlib.util.find_spec('dotenv'):
            self.supported_list = f"{self.supported_list}, {cli_bcolors.OKBLUE}ENV (r){cli_bcolors.ENDC}"
        if importlib.util.find_spec('xmltodict'):
            self.supported_list = f"{self.supported_list}, {cli_bcolors.OKBLUE}XML (r/w){cli_bcolors.ENDC}"

    @staticmethod
    def convert(input: str, input_type: str = None, output_type: str = None):
        input_type = input_type.strip().lower()
        Path(input)
        if input_type == 'yaml':
            d = yaml.safe_load(input)
        if input_type == 'json':
            d = json.loads(input)
        if input_type == 'toml':
            d = toml.loads(input)
        if input_type == 'xml':
            if importlib.util.find_spec('xmltodict'):
                import xmltodict
                d = xmltodict.parse(input, process_namespaces=True)
        if input_type == 'ini':
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            config.read_string(input)

            return parse_ini(config=config)

    @staticmethod
    def infer_read_file_type(file_path: str):
        """
        Infer the file type and return loaded contents. By default, the type is inferred from the suffix of the
        file path. Thus, `file.yaml` will be read as a YAML file. If the file extension is not known, the file will be
        read and tried to be loaded as both types.

        Raises:
             ValueError: If the type could not be inferred.

        Args:
            file_path (str): Input file path to read.

        Returns:
            dict: Loaded YAML (or JSON).
        """

        input_file = Path(file_path)

        suffix = input_file.suffix.lower() if input_file.suffix else None

        if suffix == '.json':
            with input_file.open("r") as fin:
                return json.load(fin)

        if suffix in ['.yaml', '.yml']:
            with input_file.open("r") as fin:
                return yaml.safe_load(fin)

        if suffix == '.toml':
            with input_file.open("rb") as fin:
                return toml.load(fin)

        if suffix == '.ini':
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            with input_file.open("r") as fin:
                config.read_file(fin)

            return parse_ini(config=config)


        if suffix == '.xml':
            if importlib.util.find_spec('xmltodict'):
                import xmltodict

                with input_file.open("rb") as fin:
                    return xmltodict.parse(fin, process_namespaces=True)

        if input_file.stem.lower() == '.env' or suffix == '.env':
            if importlib.util.find_spec('dotenv'):
                from dotenv import dotenv_values

                return dotenv_values(dotenv_path=str(input_file.absolute()))

        try:
            with input_file.open("r") as fin:
                return json.load(fin)
        except:
            pass

        try:
            with input_file.open("r") as fin:
                return yaml.safe_load(fin)
        except:
            pass

        try:
            with input_file.open("rb") as fin:
                return toml.load(fin)
        except:
            pass

        try:
            if importlib.util.find_spec('xmltodict'):
                import xmltodict

                with input_file.open("rb") as fin:
                    return xmltodict.parse(fin, process_namespaces=True)
        except:
            pass

        try:
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            with input_file.open("r") as fin:
                config.read_file(fin)

            return parse_ini(config=config)
        except:
            pass

        try:
            if importlib.util.find_spec('dotenv'):
                from dotenv import dotenv_values

                return dotenv_values(dotenv_path=str(input_file.absolute()))
        except:
            pass

        raise ValueError(f"Input file {input_file.name} could not be inferred")

    def do_convert(self):
        """
        Converts all input files to output type(s).
        """
        if self.input_files is None and self.input_directories is None:
            raise ValueError("Either input_files or input_directories must be defined!")

        if self.input_files is None and not self.input_directories is None:
            # set output to none as it should not be defined in this scenario
            self.output_files = None
            self.input_files = list()
            for d in self.input_directories:
                dir_path = Path(d)
                # TODO extend glo range here if expanding
                self.input_files.extend(list(dir_path.glob("*.yaml")))
                self.input_files.extend(list(dir_path.glob("*.yml")))
                self.input_files.extend(list(dir_path.glob("*.json")))
                self.input_files.extend(list(dir_path.glob("*.toml")))
                self.input_files.extend(list(dir_path.glob("*.xml")))
                self.input_files.extend(list(dir_path.glob("*.ini")))
                self.input_files.extend(list(dir_path.glob("*.env")))


        if self.output_files is None:
            self.output_files = list()
            for input_file in self.input_files:
                self.output_files.append(f"{os.path.splitext(input_file)[0]}.{self.default_output_type.lower()}")


        zipped = zip(self.input_files, self.output_files)

        for pair in zipped:
            try:
                input_data = Converter.infer_read_file_type(pair[0])
                output_file = Path(pair[1])

                suffix = output_file.suffix.lower() if output_file.suffix else f".{self.default_output_type}"

                if suffix == '.yaml':
                    with output_file.open("w") as fout:
                        yaml.safe_dump(input_data, fout)

                if suffix == '.json':
                    with output_file.open("w") as fout:
                        json.dump(input_data, fout)

                if suffix == '.toml':
                    with output_file.open("wb") as fout:
                        tomlw.dump(toml_null_stripper(input_data), fout)

                if suffix == '.xml':
                    if importlib.util.find_spec('xmltodict'):
                        import xmltodict

                        with output_file.open("wb") as fout:
                            return xmltodict.unparse(input_data, fout)
                    else:
                        raise ImportError("Missing 'xmltodict' dependency")

                if suffix == '.ini':
                    from rickled import Rickle
                    with output_file.open("w") as fout:
                        Rickle(input_data).to_ini(output=fout)

                if not self.silent:
                    print(f"{cli_bcolors.OKBLUE}{pair[0]}{cli_bcolors.ENDC} -> {cli_bcolors.OKBLUE}{pair[1]}{cli_bcolors.ENDC}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{cli_bcolors.FAIL}{str(exc)}{cli_bcolors.ENDC}")
                continue