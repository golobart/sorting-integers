import os
import logging
import array as arr
from uuid import uuid4
from pathlib import Path

import utils.messages as msg


class Slicer(object):
    """
    Slices the input file in smaller files of size nbig.

    Slice_... files are left in the slice pool
    When slicing is finished end file is signaled-touch at slice pool
    Emits warnings for each invalid number in the input file.
    """
    def __init__(self, args, conf):
        """
        Initializes attributes and makes slices.
    
        """
        self.warning_cnt = 0 # counts the warned lines in input file
        self.line_cnt = 0 # counts the number of lines in input file
        self.elems_cnt = 0 # counts inserted elements in a slice
        self.nbig = args.nbig # the number of biggest numbers to select
        self.infilename = args.input_file
        self.outfilename = args.output_file
        self.in_iter_file = self._input_file_gen(args.input_file, eval(conf["filebuffer"])) # the input file as a generator
        self.slice_pool_pathname = conf["slices_pool"] # folder pathname of slices pool

    def create_slices(self, in_numbers=None):
        """
        Slice input file and store the chunks in the slice pool.
    
        slice files are left in the slice pool named as slice_....
        Args:
            in_number: optional parameter, can be any generator of numbers in substitution of the input file, 
                       can be used in the test phase of the development process
        """
        try:
            iter_numbers = self.in_iter_file if in_numbers is None else in_numbers
    
            f_slicing = self._create_slice()
    
            for elem in iter_numbers:
                self.line_cnt += 1
    
                # check line validity as unsigned integer
                if not self._check_line(elem):
                    self.warning_cnt += 1
                    logging.warning(f"Invalid line ({self.line_cnt}) {elem}")
                    continue
    
                # if slice is full, create the next
                if self.elems_cnt == self.nbig:
                    f_slicing = self._next_slice(f_slicing)
                    self.elems_cnt = 0
                
                # Store number in slice
                f_slicing.write(elem)
                self.elems_cnt += 1
    
            self._close_slice(f_slicing)
    
            # signal end of slicing
            Path(os.path.join(self.slice_pool_pathname, msg.ENDFN)).touch(exist_ok=True)
        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            # signal end to presorter
            Path(os.path.join(self.slice_pool_pathname, msg.ENDFN)).touch(exist_ok=True)
            raise

    # TODO avoid repeated code
    def _create_slice(self):
        """
        Opens a file to store a slice of numbers.
    
        """
        f = None
        try:
            prefix = msg.SLICINGPFX
            unique_postfix = str(uuid4())
    
            fname = self.slice_pool_pathname + prefix + unique_postfix
            f = open(fname, 'w')
    
            logging.debug(f"New slicing {fname=}")
        except Exception as e:
            logging.critical(f"Failed to create slice {fname=}")
            raise
        
        return f


    def _close_slice(self, f):
        """
        Closes a slice file.
    
        File name is changed from slicing to slice
        """
        try:
            prefix = msg.SLICEDPFX

            oldfname = f.name
            unique_postfix = oldfname.split("_")[-1]
    
            newfname = self.slice_pool_pathname + prefix + unique_postfix
            f.close()
            os.rename(oldfname, newfname) # POSIX atomic operation
    
            logging.debug(f"New slice {newfname=}")
        except Exception as e:
            logging.critical(f"Failed to close slice {oldfname=}")
            raise


    def _next_slice(self, f):
        """
        Closes a slice file and generates a new one.
    
        File name is changed from slicing to slice
        """
        self._close_slice(f)
        return self._create_slice()


    # TODO avoid code repetition
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

