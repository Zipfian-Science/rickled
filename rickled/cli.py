import os

from __version__ import __version__

import argparse
from typing import List
from pathlib import Path
import yaml
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

    def infer_read_file_type(self, file_path: str):
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

        if suffix == '.yaml':
            with input_file.open("r") as fin:
                return yaml.safe_load(fin)

        if suffix is None:
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
        Does conversion.
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
                input_data = self.infer_read_file_type(pair[0])
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


def conv(args):
    Converter(input_files=args.i,
              output_files=args.o,
              input_directories=args.d,
              default_output_type=args.t,
              silent=args.s).do_convert()

def serve(args):
    from rickled.net import serve_rickle_http, serve_rickle_https
    pass

def main():
    parser = argparse.ArgumentParser(
        prog='rickle',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"""
-----------------------------------------------------
{bcolors.HEADER}YAML tools for Python{bcolors.ENDC} (version {__version__}).
""",
        epilog="-----------------------------------------------------"
    )
    parser.add_argument(
        "--version",
        "-v",
        help="show version number",
        action="version",
        version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers()

    #################### CONV #####################

    parser_conv = subparsers.add_parser('conv',
                                        help='Tool for converting files to or from YAML',
                                        description=f"""
---
{bcolors.HEADER}Tool for converting files to or from YAML{bcolors.ENDC}.
    """,
                                        epilog="-----------------------------------------------------"
                                        )

    parser_conv.add_argument('-i', type=str, help=f"{bcolors.OKBLUE}input file{bcolors.ENDC} to convert",
                             nargs='+', metavar='input')
    parser_conv.add_argument('-d', type=str, help=f"{bcolors.OKBLUE}directory{bcolors.ENDC} of files to convert",
                             default=None, nargs='+', metavar='dir')
    parser_conv.add_argument('-o', type=str, help=f"{bcolors.OKBLUE}output file{bcolors.ENDC} to convert",
                             nargs='+', metavar='output')
    parser_conv.add_argument('-t', type=str, help=f"output {bcolors.OKBLUE}file type{bcolors.ENDC} (JSON, YAML)",
                             default='yaml', metavar='type')
    parser_conv.add_argument('-s', action='store_true', help=f"{bcolors.OKBLUE}suppress{bcolors.ENDC} verbose output",)

    parser_conv.set_defaults(func=conv)

    #################### SERVE #####################

    parser_serve = subparsers.add_parser('serve',
                                        help='Tool for serving YAML via http(s)',
                                        description=f"""
    ---
    {bcolors.HEADER}Tool for serving YAML via http(s){bcolors.ENDC}.
        """,
                                        epilog="-----------------------------------------------------"
                                        )

    parser_serve.add_argument('--file', type=str, help=f"{bcolors.OKBLUE}YAML{bcolors.ENDC} or {bcolors.OKBLUE}JSON{bcolors.ENDC} file to serve")
    parser_serve.add_argument('--host', type=str, help=f"{bcolors.OKBLUE}host{bcolors.ENDC} interface")
    parser_serve.add_argument('--port', type=int, help=f"{bcolors.OKBLUE}port{bcolors.ENDC} number")
    parser_serve.set_defaults(func=serve)

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()