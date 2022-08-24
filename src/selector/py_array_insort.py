import logging
import array as arr
import bisect
import time

from selector.base_selector import Selector


class PyArrayInSsort(Selector):
    """
    Selector of top numbers based on python array.

    These arrays are made of elements of the same type and are contiguous in memory.
    Use of array.insert to store values in topn store (topn grows as values are inserted)
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
        super(PyArrayInSsort, self).__init__(args, conf)
        
                                  

    def select_nbig(self, in_numbers=None):
        """
        Implements selection of largest numbers using bynary search (Python bisect) and sorted inserting (array.insert).
    
        Leaves self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            in_numbers: (optional) source to read input numbers from, by default as an iterator of args.input_file.
                       can be any generator of numbers in substitution of the input file, 
                       can be used in the test phase of the development process
        """
        self.topn = arr.array("Q") # the store, array of 8 bytes elements, unsigned long long
        self._store_array_report()

        iter_numbers = self.in_iter_file if in_numbers is None else in_numbers

        # initialize first element
        #self._init_first_element(iter_numbers)

        for elem in iter_numbers:
            self.line_cnt += 1

            # TODO parametrize in some way for monolithic and parallel
            # check line validity as unsigned integer
            # if not self._check_line(elem):
            #     self.warning_cnt += 1
            #     logging.warning(f"Invalid line ({self.line_cnt}) {elem}")
            #     continue

            # get index to insert and num of elements in store (always sorted)
            x = int(elem)
            index = bisect.bisect_right(self.topn, x)
            num_elems = len(self.topn)
            #num_elems = self.elems_cnt  # , lo=0, hi=self.elems_cnt

            # if self.line_cnt > 990000: # just basic profiling
            #    t = time.process_time_ns()
            #    #t = time.perf_counter_ns()

            # seek topn index where new value x could be inserted
            #index = bisect.bisect_right(self.topn, x, lo=0, hi=num_elems)
            # if self.line_cnt > 990000: # just basic profiling
            #     elapsed_time = time.process_time_ns() - t
            #     #elapsed_time = time.perf_counter_ns() - t
            #     logging.debug(f"BISECT {elapsed_time=}")

            #logging.debug(f"{index=} {num_elems=}")

            # check if the new number is already in store
            ###repeated = True if self.topn[index-1] == x else False
            #logging.debug(f"New value {'REPEATED' if repeated else ''} {x=} {self.topn=}")
            ###if repeated: # is a repetition
            ###    if self.allow_repeats: # insert only if repetitions are allowed
            ###        self._try_to_store(index, x, num_elems)
                # else:
                #     logging.debug(f"REPETITIONS NOT allowed {x=} {self.topn=}")
            ###else: # no repeated, try to store
                ###self._try_to_store(index, x, num_elems)
            self._try_to_store(index, x, num_elems)
        
        # unfortunately bisect only works in asccending order
        logging.debug(f"Reversing topn array")
        self.topn.reverse()
        
        self._store_array_report()


    def _try_to_store(self, index, value, num_elems):
        """
        Try to store in array topn the new value only.
    
        Value has already been checked to be a positive integer and repetitions could be filtered out.
        Value is always stored if topn array is not at its full capacity (nbig), but if topn store is full,
        the new vaue is inserted only if it is bigger than the minor value in store.
        Args:
            index: topn store index where value could be inserted.
            value: new value to insert in topn.
            num_elems: number of values already stored in topn.
        """
        if  self.nbig > num_elems: # store is not full at max capacity nbig, so insert it
            self._store_number(index, value, num_elems)

            # if self.line_cnt > 990000: # just basic profiling
            #    t = time.process_time_ns()
            #    #t = time.perf_counter_ns()
            #self.topn.insert(index, value)
            #self.topn.pop()
            # if self.line_cnt > 990000: # just basic profiling
            #     elapsed_time = time.process_time_ns() - t
            #     #elapsed_time = time.perf_counter_ns() - t
            #     logging.debug(f"INSERT POP LAST {elapsed_time=}")

            
            self.elems_cnt += 1
            #logging.debug(f"topn growing, inserted {value=} {self.topn=}")
        else:
            # topn is already at its max capacity nbig, do not insert if new value is lower than lowest in store
            # if value <= self.topn[0]: 
            #     logging.debug(f"topn full, lower element not inserted {value=} {self.topn=}")
            # else:
            if value > self.topn[0]: 
                self._store_number(index, value, num_elems)
                self.topn.pop(0)
                
                # if self.line_cnt > 990000: # just basic profiling
                #    t = time.process_time_ns()
                #    #t = time.perf_counter_ns()
                #self.topn.insert(index, value)
                #self.topn.pop(0)
                # if self.line_cnt > 990000: # just basic profiling
                #     elapsed_time = time.process_time_ns() - t
                #     #elapsed_time = time.perf_counter_ns() - t
                #     logging.debug(f"INSERT POP FIRST {elapsed_time=}")
                # #logging.debug(f"topn full, inserted {value=} {self.topn=}")


    def _store_number(self, index, value, num_elems):
        """
        Stores value at index position in topn.
    
        We have to distinguish between insert or appending at the end.
        Args:
            index: topn store index where value could be inserted.
            value: new value to insert in topn.
            num_elems: number of values already stored in topn.
        """
        if index < num_elems:
            self.topn.insert(index, value)
        else:
            self.topn.append(value)
        #self.elems_cnt += 1


    def _init_first_element(self, iter_numbers):
        for elem in iter_numbers:
            self.line_cnt += 1

            # TODO parametrize in some way for monolithic and parallel
            # check line validity as unsigned integer
            # if not self._check_line(elem):
            #     self.warning_cnt += 1
            #     logging.warning(f"Invalid line ({self.line_cnt}) {elem}")
            #     continue

            # get index to insert and num of elements in store (always sorted)
            x = int(elem)
            self.topn.append(x)
            logging.debug(f"FIRST {x=}")
            self.elems_cnt += 1
            break