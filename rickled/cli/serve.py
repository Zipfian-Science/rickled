import sys
import warnings
from rickled.tools import CLIError

from rickled import Rickle, UnsafeRickle

def serve(args):
    try:
        from rickled.net import serve_rickle_http
    except NameError:
        warnings.warn('Required Python package "twisted" not found.', ImportWarning)
        return

    output_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'json'
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

        if args.BROWSER:
            import webbrowser

            scheme = 'https' if args.CERTIFICATE and args.PRIVATE_KEY else 'http'
            webbrowser.open(f'{scheme}://{args.HOST}:{args.PORT}', new=2)

        serve_rickle_http(rickle=rick,
                          port=args.PORT,
                          interface=args.HOST,
                          serialised=args.SERIALISED,
                          output_type=output_type,
                          path_to_certificate=args.CERTIFICATE,
                          path_to_private_key=args.PRIVATE_KEY,
                        )
    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.SERVE)
