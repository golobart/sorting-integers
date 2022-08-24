import argparse
from os import access, R_OK
from os.path import isfile, isdir

import utils.messages as msg


# TODO possible use of decorators
def get_args():
    """
    Get command line arguments of main.py.

    Obtained from the command line: python main.py -n <number> -if <input file> -of <output file>
    Returns:
        args: Parsed arguments, can be accessed like attributes i.e. arg.nbig .
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nbig", default=10, type=int, action=CabUInt, help=msg.HELPNBIG)
    parser.add_argument("-if", "--input-file", action=CabInFile,  required=True, help=msg.HELPFINPUT) # type=open,
    parser.add_argument("-of", "--output-file", required=True, help=msg.HELPFOUT)
    args = parser.parse_args()

    return args


class CabInFile(argparse.Action):
    """
    Check correctness of input file argument.
    
    """
    def __call__(self, parser, namespace, values, option_string=None):
        # check if file exists
        if not isfile(values):
            raise argparse.ArgumentError(self, f'{msg.ERRFINPNOEXIST} ({values})')
        if not access(values, R_OK):
            raise argparse.ArgumentError(self, f'{msg.ERRFINPNOREAD} ({values})')
        setattr(namespace, self.dest, values)


class CabUInt(argparse.Action):
    """
    Check correctness of number of top results argument.
    
    """
    def __call__(self, parser, namespace, values, option_string=None):
        # check if file exists
        if values <= 0:
            raise argparse.ArgumentError(self, f'{msg.ERRNEGATIVE} ({values})')
        if values > 30000000:
            raise argparse.ArgumentError(self, f'{msg.ERRTOOBIG} ({values})')
        setattr(namespace, self.dest, values)
