import os
import logging
import array as arr



class Selector(object):
    """
    Base class for selectors of top largest numbers.


    """
    def __init__(self, args, conf):
        """
        Base init method, gets configuration and command lines.
    
        Has to leave self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            args: command line arguments.
            conf: General section of config.ini file
        """
        self.reset() # Initializes counters and topn
        self.nbig = args.nbig # the number of biggest numbers to select
        self.allow_repeats = bool(int(conf["allow_repeats"])) # allow or not repeated numbers in the topn results
        self.infilename = args.input_file
        self.outfilename = args.output_file
        self.in_iter_file = self._input_file_gen(args.input_file, conf["filebuffer"]) # the input file as a generator

    def select_nbig(self, in_numbers=None):
        """
        Base method to implement the selection.
    
        Has to leave self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            in_numbers: source to read input numbers from, by default as an iterator.
        Returns:
        Note:
        """
        pass
# TODO testing and profiling
# TODO cache to avoid start from begining if crash or distribute load among nodes
# more time and input file example



    def result_report(self):
        """
        Prints a basic final report.
    
        """
        logging.info(f"-----------result report----------------")
        logging.info(f"Input file {self.infilename}")
        logging.info(f"Invalid lines in file {self.warning_cnt}")
        logging.info(f"Total lines in file {self.line_cnt}")
        logging.info(f"Output file {self.outfilename}")
        logging.info(f"Number of elements inserted {self.elems_cnt}")
        logging.info(f"----------------------------------------")

    def reset(self):
        """
        Reinitializes counters and topn.
    
        """
        self.topn = None # the store, where the largest numbers will be stored
        self.warning_cnt = 0 # counts the warned lines in input file
        self.elems_cnt = 0 # counts inserted elements in store
        self.line_cnt = 0 # counts the number of lines in input file


    def _store_array_report(self):
        """
        Prints a basic status report of array store topn.
    
        """
        logging.debug(f"--------store array report--------------")
        logging.debug(f"{arr.typecodes=}")
        logging.debug(f"{self.topn.typecode=}")
        logging.debug(f"{self.topn.itemsize=}")
        logging.debug(f"{self.topn.buffer_info()=}")
        logging.debug(f"{self.topn.buffer_info()[1] * self.topn.itemsize=}")
        logging.debug(f"----------------------------------------")


    def _input_file_gen(self, in_file, buf_size):
        """
        Opens input file in a context.
    
        Context automatically closes input file when done.
        Input numbers can be read from this generator as an iterable.
        Limiting buffering to buf_size, avoid memory issues with large input files.
        Args:
            in_file: name of the input file to open.
            buf_size: size of the in_file memory buffer.
        """
        with open(in_file, 'r', buffering=int(buf_size)) as f:
            for line in f:
                yield(line)


    def _write_output_file(self, out_file):
        """
        Creates the output file and the path if it does not exists.
    
        Args:
            out_file: name of the output file.
        """
        pname = os.path.dirname(out_file)
        nl = "\n"
        # TODO check it at the begining, we do not want spend time sorting and at the end lose the sorted file!!!
        if pname != "":
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "w") as f:
            for num in self.topn:
                f.write(f"{num}{nl}")



    def _check_line(self, line: str):
        """
        Check if line contains a str representing a positive integer.
    
        Before checking, strips out white spaces and newlines from both sides.
        Args:
            line: string containing the input to check.
        returns:
            True if line contains a positive integer, False otherwise.
        """
        return True if line.strip().isdigit() else False
        # valid = True
        # if isinstance(line.rstrip(), int):
        #     if line < 0:
        #         valid = False
        # else:
        #     valid = False

        # return valid

