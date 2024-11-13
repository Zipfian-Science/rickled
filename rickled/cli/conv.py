import sys
from rickled.tools import CLIError
from rickled.tools import Converter

def conv(args):
    try:
        if args.INPUT or args.INPUT_DIRECTORY:
            Converter(input_files=args.INPUT,
                      output_files=args.OUTPUT,
                      input_directory=args.INPUT_DIRECTORY,
                      default_output_type=args.OUTPUT_TYPE,
                      verbose=args.VERBOSE).do_convert()
        elif args.OUTPUT_TYPE:
            data = sys.stdin.read()

            converted = Converter.convert_string(input_string=data,
                                                 input_type=args.INPUT_TYPE,
                                                 output_type=args.OUTPUT_TYPE)

            print(converted)
        else:
            raise CLIError(message='Incorrect usage of CLI tool, refer to documentation', cli_tool=CLIError.CLITool.CONV)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.CONV)
