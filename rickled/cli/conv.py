import sys
from rickled.tools import CLIError
from rickled.tools import Converter

def conv(args):
    try:
        output_type = args.OUTPUT_TYPE.lower() if args.OUTPUT_TYPE else 'yaml'
        if args.INPUT or args.INPUT_DIRECTORY:
            Converter(input_files=args.INPUT,
                      output_files=args.OUTPUT,
                      input_directory=args.INPUT_DIRECTORY,
                      default_output_type=output_type,
                      verbose=args.VERBOSE).do_convert()
        else:
            data = sys.stdin.read()

            converted = Converter.convert_string(input_string=data,
                                                 input_type=args.INPUT_TYPE,
                                                 output_type=output_type)

            print(converted)

    except Exception as exc:
        raise CLIError(message=str(exc), cli_tool=CLIError.CLITool.CONV)
