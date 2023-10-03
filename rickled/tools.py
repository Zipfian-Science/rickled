from typing import List, Union
from pathlib import Path
import yaml
import json
import os

class bcolors:
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

    def __init__(self,
                 input_files: List[str] = None,
                 input_directories: List[str] = None,
                 schema: Union[str, dict] = None,
                 output_dir: str = None,
                 silent: bool = False,
                 ):
        self.input_files = input_files
        self.input_directories = input_directories

        if isinstance(schema, str):
            self.schema = Converter.infer_read_file_type(schema)
        else:
            self.schema = schema

        self.output_dir = output_dir

        self.silent = silent

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
                self.input_files.extend(list(dir_path.glob("*.json")))


        self.output_files = list()
        for input_file in self.input_files:
            self.output_files.append(f"{os.path.splitext(input_file)[0]}.schema.yaml")


        zipped = zip(self.input_files, self.output_files)

        for pair in zipped:
            try:
                input_data = Converter.infer_read_file_type(pair[0])
                output_file = Path(pair[1])

                schema = Schema.generate_schema_from_obj(input_data)

                with output_file.open("w") as fout:
                    yaml.safe_dump(schema, fout)

                if not self.silent:
                    print(f"{bcolors.OKBLUE}{pair[0]}{bcolors.ENDC} -> {bcolors.OKBLUE}{pair[1]}{bcolors.ENDC}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{bcolors.FAIL}{str(exc)}{bcolors.ENDC}")
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
                self.input_files.extend(list(dir_path.glob("*.json")))

        for file in self.input_files:
            try:
                input_data = Converter.infer_read_file_type(file)

                passed = Schema.schema_validation(input_data, self.schema, no_print=self.silent)

                if not passed:
                    failed_validation.append(file)

                if not self.silent:
                    result = f"{bcolors.OKGREEN}OK{bcolors.ENDC}" if passed else f"{bcolors.FAIL}FAIL{bcolors.ENDC}"
                    print(f"{bcolors.OKBLUE}{file}{bcolors.ENDC} -> {result}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{bcolors.FAIL}{str(exc)}{bcolors.ENDC}")
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
            schema = dict()
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

        if value == str:
            return {'type': 'str'}
        if value == int:
            return {'type': 'int'}
        if value == float:
            return {'type': 'float'}
        if value == bool:
            return {'type': 'bool'}
        if value is None:
            return {'type': 'any'}

        if isinstance(value, dict):
            named_schema = {'type': 'dict', 'schema': dict()}
            for k, v in value.items():
                named_schema['schema'][k] = Schema._data_types_to_schema(v)
            return named_schema

        if isinstance(value, list):
            named_schema = {'type': 'list', 'schema': list()}
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
    def schema_validation(obj, schema: dict, path: str = 'root', no_print: bool = False) -> bool:
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
                new_path = f"{new_path}->{k}"
                req = v.get('required', False)
                nullable = v.get('nullable', False)
                present = k in obj.keys()
                if not present:
                    if req:
                        if not no_print:
                            print(f"Required {bcolors.FAIL}'{k}'{bcolors.ENDC} (per schema {v}),\n In {obj},\n Path {bcolors.WARNING}{new_path}{bcolors.ENDC}")
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
                        f"Type '{k}' == {bcolors.FAIL}'{type(obj[k]).__name__}'{bcolors.ENDC},\n Required type {bcolors.OKBLUE}'{v['type']}'{bcolors.ENDC} (per schema {v}),\n In {obj},\n Path {bcolors.WARNING}{new_path}{bcolors.ENDC}")
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
                    f"Length '{obj}' == {bcolors.FAIL}{obj_length}{bcolors.ENDC},\n Required length {bcolors.OKBLUE}{length}{bcolors.ENDC} (per schema {schema['schema']}),\n In {obj},\n Path {bcolors.WARNING}{new_path}{bcolors.ENDC}")
                return False

            if schema_len > 0:
                single_type = schema['schema'][0]

                for i in range(obj_length):
                    new_path = f"{new_path}->[{i}]"
                    o = obj[i]
                    if single_type['type'] != 'any' and type(o).__name__ != single_type['type']:
                        if not no_print:
                            print(
                            f"Type '{o}' == {bcolors.FAIL}'{type(o).__name__}'{bcolors.ENDC},\n Required type {bcolors.OKBLUE}'{single_type['type']}'{bcolors.ENDC} (per schema {single_type}),\n In {o},\n Path {bcolors.WARNING}{new_path}{bcolors.ENDC}")
                        return False
                    if single_type['type'] in ['dict', 'list']:
                        if not Schema.schema_validation(o, single_type, path=new_path, no_print=no_print):
                            return False
                    new_path = path
            return True

class Converter:
    """
    Tool for converting between YAML and JSON, mainly to be used in CLI.

    Args:
        input_files (list): List of input file paths (default = None).
        input_directories (list): List of directories (default = None).
        output_files (list): List of output file paths (default = None).
        default_output_type (str): Default type to convert to if output files are not provided (default = 'yaml').
        silent (bool): Suppress verbose output (default = None).
    """

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

        try:
            with input_file.open("r") as fin:
                return json.load(fin)
        except:
            pass

        try:
            with input_file.open("r") as fin:
                return yaml.safe_load(fin)
        except:
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
                self.input_files.extend(list(dir_path.glob("*.yaml")))
                self.input_files.extend(list(dir_path.glob("*.json")))


        if self.output_files is None:
            self.output_files = list()
            for input_file in self.input_files:
                self.output_files.append(f"{os.path.splitext(input_file)[0]}.{self.default_output_type}")


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

                if not self.silent:
                    print(f"{bcolors.OKBLUE}{pair[0]}{bcolors.ENDC} -> {bcolors.OKBLUE}{pair[1]}{bcolors.ENDC}")
                continue
            except Exception as exc:
                if not self.silent:
                    print(f"{bcolors.FAIL}{str(exc)}{bcolors.ENDC}")
                continue