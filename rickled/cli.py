import rickled.__version__ as ver
import argparse

from rickled.tools import bcolors

def conv(args):
    from rickled.tools import Converter
    Converter(input_files=args.i,
              output_files=args.o,
              input_directories=args.d,
              default_output_type=args.t,
              silent=args.s).do_convert()

def serve(args):
    from rickled.net import serve_rickle_http, serve_rickle_https
    from rickled import Rickle


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
    from rickled.tools import Schema
    Schema(input_files=args.i,
           input_directories=args.d,
           schema=args.c,
           output_dir=args.o,
           silent=args.s).do_validation()

def gen(args):
    from rickled.tools import Schema
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

    #################### SERVE #####################

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

    #################################################

    #################### SCHEMA - GEN ############
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