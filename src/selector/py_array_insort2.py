import logging
import array as arr
import bisect
import time

from selector.base_selector import Selector


class PyArrayInSsort2(Selector):
    """
    Selector of top numbers based on python array.

    These arrays are made of elements of the same type and are contiguous in memory.
    Use of bisect.insort to store values in topn store (topn grows as values are inserted)
    Note:
        No good performance when args.nbig is over 1.000.000, too much memory is moved for insertions
    """
    def __init__(self, args, conf):
        """
        Initializes topn store as a Python array at its max capacity (args.nbig).
    
        Has to leave self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            args: command line arguments.
            conf: General section of config.ini file
        """
        super(PyArrayInSsort2, self).__init__(args, conf)
        self.topn = arr.array("Q") # the store, array of 8 bytes elements, unsigned long long
                                  

    def select_nbig(self, in_numbers=None):
        """
        Implements selection of largest numbers using bynary search and sorted inserting (bisect.insort).
    
        Leaves self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            in_numbers: source to read input numbers from, by default as an iterator of args.input_file .
        """
        self._store_array_report()
        logging.debug(f"Attention!! insort method does not control repetitions")
        logging.debug(f"----------------------------------------")

        iter_numbers = self.in_iter_file if in_numbers is None else in_numbers

        for elem in iter_numbers:
            self.line_cnt += 1

            # check line validity as unsigned integer
            if not self._check_line(elem):
                self.warning_cnt += 1
                logging.warning(f"Invalid line ({self.line_cnt}) {elem}")
                continue

            # get index to insert and num of elements in store (always sorted)
            x = int(elem)
            num_elems = len(self.topn)
            #logging.debug(f"{num_elems=}")
            if  self.nbig > num_elems:
                bisect.insort_left(self.topn, x)
                self.elems_cnt += 1
                #logging.debug(f"topn growing, imserted {x=} {self.topn=}")
            else:
                if x <= self.topn[0]: # optimization in case topn is already at its max length nbig
                    #logging.debug(f"topn full, lower element not inserted {x=} {self.topn=}")
                    pass
                else:
                    bisect.insort_left(self.topn, x)
                    self.topn.pop(0)
                    #logging.debug(f"topn full, inserted {x=} {self.topn=}")
