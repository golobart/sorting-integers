import logging
import os, time
import array as arr
from math import ceil
from pathlib import Path
from selector.factory import get_selector

import utils.messages as msg

class Presorter(object):
    """
    Process all the slice files in the slice pool and leaves them sorted in the consolidation pool (sorted descending).

    Presorting is the iterative process to get each slice file (of nbig numbers each), sort it and leaves it as presorted_...
    in the consolidation pool. 
    presorted_.... files are ready to be consolidated in the next consolidation phase
    """
    def __init__(self, args, conf):
        """
        Base init method, gets configuration and command lines.
    
        Args:
            args: command line arguments.
            conf: General section of config.ini file
        """
        self.bucket_size = int(eval(conf["bucket_average"]))
        self.filebuffer = int(eval(conf["filebuffer"]))
        self.nbig = args.nbig # the number of biggest numbers to select
        
        # self.topn.itemsize is 8 for Q arrays
        self._shift = arr.array("Q").itemsize * 8
        self.number_of_buckets = 1
        if args.nbig >= self.bucket_size:
            self.number_of_buckets = self._good_numbers_of_buckets()
            self._shift -= (self.number_of_buckets.bit_length() - 1) 
            
        self.topn = None # the store, where the largest numbers will be stored
        #self.warning_cnt = 0 # counts the warned lines in input file
        self.elems_cnt = 0 # counts inserted elements in store
        self.line_cnt = 0 # counts the number of lines in input file
        
        #self.allow_repeats = bool(int(conf["allow_repeats"])) # allow or not repeated numbers in the topn results
        #self.infilename = args.input_file
        #self.outfilename = args.output_file
        #self.in_iter_file = self._input_file_gen(args.input_file, conf["filebuffer"]) # the input file as a generator
        self.slice_pool_pathname = conf["slices_pool"] # folder pathname of slices pool
        self.consolidation_pool_pathname = conf["consolidation_pool"] # folder pathname of slices pool
        self.buckets = self._create_buckets()
        self.selector = get_selector(args, conf)

    def sort_pool(self):
        """
        Sorts all slice files in the slice pool.
    
        Sorted files are left in the consolidation pool named as presorted_....
        Terminates when there is only end file in the pool.
        """
        try:
            is_this_the_end = False
            while not is_this_the_end:
                slice_name = self._get_slice()
                if slice_name:
                    self.sort_slice(slice_name)
                else: # check for end
                    time.sleep(1)
                    is_this_the_end = self._check_end()
            else:
                # signal end to consolidator
                Path(os.path.join(self.consolidation_pool_pathname, msg.ENDFN)).touch(exist_ok=True)
        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            # signal end to consolidator
            Path(os.path.join(self.consolidation_pool_pathname, msg.ENDFN)).touch(exist_ok=True)
            raise

    def _check_end(self):
        """
        Checks if the presort phase is finished.
    
        End is reached when in the slice pool contains only one file named end
        """
        the_end = False
        num_of_files = 0
        for fname in os.listdir(self.slice_pool_pathname):
            if fname == msg.ENDFN:
                the_end = True
            num_of_files += 1

        return the_end and num_of_files == 1


    def sort_slice(self, slice_name):
        """
        Gets one slice file (slice_....) of the slice pool, sorts and output it to the consolidation pool (presorted_....).

        To speed the sort the slice is bucketized, on each bucket the sorting algorithm (selector class) is applied.
        Args:
            slice_name: the path+name of the slice file to be sorted
        """
        try:
            in_iter_slice = self._input_file_gen(slice_name, self.filebuffer)
            self.buckets = self._create_buckets()
            self._fill_buckets(in_iter_slice)
            for bucket in self.buckets:
                self.selector.reset()
                self.selector.select_nbig(self.buckets[bucket]) # sort the bucket
                self.buckets[bucket] = self.selector.topn # replace original bucket by its sorted version
                
            # save sorted slice to consolidation pool
            self._save_sorted_slice(slice_name)
        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            logging.error(f"{slice_name} - try to get next slice")


    def _save_sorted_slice(self, slice_name):
        """
        Writes a sorted file joining all sorted buckets.

        File name is stored as presorted_.... in the consolidation pool, the original file (presorting_....) is removed from slice pool.
        If renaming fails the show must NOT go on because final sorting wont be right
        Args:
            slice_name: the path+name of the slice file to be sorted (presorting_...)
        """
        try:
            nl = "\n"
            os.remove(slice_name)
            old_path_name = os.path.split(slice_name)
            new_name = os.path.join(self.consolidation_pool_pathname, old_path_name[1])
            with open(new_name, 'w') as f:
                # write all sorted buckets to file (last bucket first)
                for i in range(0, self.number_of_buckets):
                    f.write(nl.join([str(x) for x in self.buckets[self.number_of_buckets - 1 -i]]))
                    f.write(nl)
            name = self._rename_file(self.consolidation_pool_pathname, old_path_name[-1], 
                              self.consolidation_pool_pathname, msg.PRESORTEDPFX)
            if not name:
                logging.error(f"Failed renaming slice from  {slice_name=} to {new_name}")
                raise ValueError(f"Renaming a sorted slice failed from {slice_name} to {new_name}")

        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            raise


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


    def _get_slice(self):
        """
        Gets a slice or file from de slice pool.
    
        If renaming fails the show must go on, may be a parallel presorter got the file just before, so look for the next
        Returns: the name of the slice file renamed to be presorted (prefix presorting_), empty string if renaming fails
        """
        # TODO control error if rename fails
        newfname = ""
        for fname in os.listdir(self.slice_pool_pathname):
            if fname.startswith(msg.SLICEDPFX): # get sliced files only, avoid files slicing_
                newfname = self._rename_file(self.slice_pool_pathname, fname, self.slice_pool_pathname, msg.PRESORTINGPFX)
                break

        return newfname

    # TODO avoid repeated code 
    def _rename_file(self, old_path, old_name, new_path, new_prefix):
        """
        Renames a file where its name is made of <prefix>_<unique_id> to a new path and prefix but keeps the unique_id.
    
        Args:
            old_path: original path
            old_name: original name as <prefix>_<unique_id>
            new_path: new path
            new_prefix: new name as <new_prefix>_<unique_id>
        returns: the new name of the file or empty string if renaming fails
        """
        newfname = ""
        try:
            oldfname = old_path + old_name
            newfname = self._reprefix_file(old_path, old_name, new_path, new_prefix)
            os.rename(oldfname, newfname) # POSIX atomic operation
        except OSError as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            newfname = ""

        return newfname

    # TODO avoid repeated code 
    def _reprefix_file(self, old_path, old_name, new_path, new_prefix):
        oldfname = old_path + old_name
        unique_postfix = old_name.split("_")[-1]
        newfname = new_path + new_prefix + unique_postfix

        return newfname



    def _create_buckets(self):
        """
        Creates a dictionary of buckets.
    
        Each bucket is a Python array
        """
        buckets = None
        if self.number_of_buckets > 0:
            buckets = {x: arr.array("Q") for x in range(self.number_of_buckets)}

        return buckets


    def _fill_buckets(self, iter_slice):
        """
        Fills the buckets with the numbers/elements in the slice.
    
        Args:
            iter_slice: generator of elements in the slice file.
        """
        for elem in iter_slice:
            num = int(elem)
            index = num >> self._shift
            self.buckets[index].append(num)


    def _good_numbers_of_buckets(self):
        """
        Calculates the best number of buckets.
    
        The best is the next power of 2 of nbig/bucket_size, because the index of the bucket for an element
        will be calculated as a bit shift instead of a div index = num/(2**64 / num_of_buckets) (low rounded)
        but if num_of_buckets is 2**k then index = num >> (64-k)
        
        returns: the best number of buckets, a power of 2
        """
        min_number_of_buckets = ceil(self.nbig / self.bucket_size)
        num_of_bits = min_number_of_buckets.bit_length()
        good_number_of_buckets = 2**num_of_bits

        return good_number_of_buckets