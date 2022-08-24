import logging
import os, time
import array as arr
import uuid
import sys
from pathlib import Path

import utils.messages as msg

class Consolidator(object):
    """
    Process all files in the consolidation pool to make the last output file (contains the nbig numbers sorted descending).

    Consolidation is the iterative process to get two sorted files (of nbig numbers each) and produce a third file 
    containing the nbig max numbers from both (sorted)
    """
    def __init__(self, args, conf):
        """
        Gets configuration parameters.
    
        """
        #self.bucket_size = int(eval(conf["bucket_average"]))
        self.filebuffer = int(eval(conf["filebuffer"]))
        self.nbig = args.nbig # the number of biggest numbers to select
        #self.number_of_buckets = 1
        #self._shift = 0
        # not worth to bucketize if there is not at least 2 buckets
        # if args.nbig >= self.bucket_size:
        #     self.number_of_buckets = self._good_numbers_of_buckets()
        #     # self.topn.itemsize is 8 for Q arrays
        #     self._shift = (arr.array("Q").itemsize * 8) - (self.number_of_buckets.bit_length() - 1) 
            
        self.topn = None # the store, where the largest numbers will be stored
        #self.warning_cnt = 0 # counts the warned lines in input file
        #self.elems_cnt = 0 # counts inserted elements in store
        #self.line_cnt = 0 # counts the number of lines in input file
        
        #self.allow_repeats = bool(int(conf["allow_repeats"])) # allow or not repeated numbers in the topn results
        #self.infilename = args.input_file
        self.outfilename = args.output_file
        self.slice_pool_pathname = conf["slices_pool"] # folder pathname of slices pool
        self.consolidation_pool_pathname = conf["consolidation_pool"] # folder pathname of slices pool
        # self.buckets = self._create_buckets()
        # self.selector = get_selector(args, conf)

    def consolidate_pool(self):
        """
        Consolidates all presorted and consolidated files (in pairs) in the consolidation pool.
    
        Terminates when there is only end file in the pool.
        If the pool only contains end file and one consolidated_... file, copies consolidated_... to destination and terminates
        """
        try:
            # is_this_the_end = False
            # while not is_this_the_end:
            #     # consolidate two
            #     self.consolidate_two()
            #     # Get info for end of consolidation phase
            #     the_end, num_files, cons_name = self._check_end()
            #     # Check end condition 
            #     if the_end and (1 <= num_files <= 2):
            #         # if necessary, copy last consolidated file to the destination
            #         self._cleanup_consolidator(cons_name)
            #         is_this_the_end = True

            is_this_the_end = False
            while not is_this_the_end:
                files = self._get_two_to_consolidate()
                if files:
                    self.consolidate_two(files)
                else: # check for end
                    time.sleep(1)
                    # Get info for end of consolidation phase
                    the_end, num_files, cons_name = self._check_end()
                    # Check end condition 
                    if the_end and (1 <= num_files <= 2):
                        # if necessary, copy last consolidated file to the destination
                        self._cleanup_consolidator(cons_name)
                        is_this_the_end = True
            else:
                # signal end to consolidator
                Path(os.path.join(self.consolidation_pool_pathname, msg.ENDFN)).touch(exist_ok=True)


        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            raise                


    def _cleanup_consolidator(self, cons_name=None):
        """
        Moves the last consolidated file to the destination.
    
        Args:
            cons_name: the name, if any, of the file in the consolidation pool to copy to the destination
        """
        if cons_name:
            # Avoid problems if orig and dest are in different partitions, copy and remove file instead of use os.rename()
            name_orig = os.path.join(self.consolidation_pool_pathname, cons_name)
            forig = open(name_orig, 'r', buffering=int(self.filebuffer))
            fdest = open(self.outfilename, 'w', buffering=int(self.filebuffer))
            fdest.write(forig.read())
            fdest.close()
            forig.close()
            os.remove(name_orig)


    def _check_end(self):
        """
        Informs about the end of the consolidation phase.
    
        End is reached in the following cases:
          a) consolidation pool contains only 2 files : the end file and one consolidated_.... file. (the first consolidator finding this condition
          have to copy consolidated_... to the destination and finish)
          b) cosolidation pool contains only the end file (think about when there s more than one consolidator running, this condition is just for finish)
        Returns: if the end file exists , num of files in the pool, name of consolidated_... file
        """
        the_end = False
        num_of_files = 0
        cons_name = ''
        for fname in os.listdir(self.consolidation_pool_pathname):
            if fname == "end":
                the_end = True
            if fname.startswith(msg.CONSOLIDATEDPFX):
                cons_name = fname
            num_of_files += 1

        return the_end, num_of_files, cons_name


    def consolidate_two(self, files):
        """
        Gets two files of the consolidation pool and consolidates-combines in just one new file containing the nbig max numbers from both.

        Candidates to be consolidated are presorted_.... and consolidated_.... files
        The two consolidated files are removed, only remains the new consolidated file.
        """
        # files = self._get_two_to_consolidate()
        if files:
            # Prepare files to be read
            in_iter_cons1 =  open(files[0], 'r', buffering=int(self.filebuffer))
            in_iter_cons2 = open(files[1], 'r', buffering=int(self.filebuffer))

            # array to store consolidated values
            cons_arr = arr.array("Q")

            # initialize with the first element of each file to consolidate
            str1, val1, iter1_active = self._get_next_cons(in_iter_cons1)
            str2, val2, iter2_active = self._get_next_cons(in_iter_cons2)

            # Each iteration gets the max of one file or the other
            for i in range(0, self.nbig):
                if iter1_active and iter2_active:
                    if val1 >= val2:
                        max = str1
                        maxint = val1
                        str1, val1, iter1_active = self._get_next_cons(in_iter_cons1)
                    else:
                        max = str2
                        maxint = val2
                        str2, val2, iter2_active = self._get_next_cons(in_iter_cons2)
                elif iter1_active:
                    max = str1
                    maxint = val1
                    str1, val1, iter1_active = self._get_next_cons(in_iter_cons1)
                elif iter2_active:
                    max = str2
                    maxint = val2
                    str2, val2, iter2_active = self._get_next_cons(in_iter_cons2)
                else:
                    break
                #write max to array of consolidaated values
                cons_arr.append(maxint) 
                #logging.debug(f"{max=}")

            # Write consolidated values to file consolidated_....
            fname = self._create_consolidating_file()
            self._save_consolidated_values(fname, cons_arr)
            self._close_consolidating_file(fname)

            # remove the two input files consolidating_....
            in_iter_cons1.close()
            in_iter_cons2.close()
            os.remove(files[0])
            os.remove(files[1])


    def _get_next_cons(self, iter):
        """
        Reads the next line in the file.

        End of file is signalized with iter_active to False.
        Returns:
            value: the value read as str (empty str at end of file)
            valint: the value read as integer (-1 at end of file)
            iter_acive: False if reached end of file, True otherwise
        """
        #value = ''
        valint = -1
        iter_active = True
        # try:
        #     value = next(iter) 
        #     valint = int(value)
        # except StopIteration:
        #     iter_active = False
        value = iter.readline()
        if len(value) > 0:
            valint = int(value)
        else:
            iter_active = False

        return value, valint, iter_active

    def _save_consolidated_values(self, ofile, cons_arr):
        """
        Saves the array of consolidated values to a consolidated file.

        The consolidation of two files writes the values to an intermediate array that must be writen to a file.
        """
        try:
            nl = "\n"
            for x in cons_arr:
                ofile.write(f"{str(x)}{nl}")
        except Exception as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            raise


    def _get_two_to_consolidate(self):
        """
        Tries to get two sorted files to be consolidated in one.
    
        The combinations of files to be consolidated are:
            two presorted files
            one presorted and one consolidated files
            two consolidated files
        returns: a list of two files to be consolidatd (both are renamed to consolidating_....), if no files are found returns an empty list.
        The returned list contains 0 or 2 files, but not 1
        """
        got_files = []

        # Try to get two presorted files
        fname = self._get_presorted()
        if fname:
            got_files.append(fname)
            fname = self._get_presorted()
            if fname:
                got_files.append(fname)

        # Try to get as many consolidated files as you need 
        if len(got_files) < 2:
            fname = self._get_consolidated()
            if fname:
                got_files.append(fname)
                if len(got_files) == 1:
                    fname = self._get_consolidated()
                    if fname and len(got_files) < 2:
                        got_files.append(fname)

        # If only got one file then rollback it to the original name
        if len(got_files) == 1:
            self._rollback_fname(got_files[0])
            got_files = []

        return got_files


    def _rollback_fname(self, fname):
        """
        Rollback the name of a file.

        if the file name prefix ends with *ing changes it to *ed
        The original name is <chars>ing_<unique_id> the rolled back name is <chars>ed_<unique_id>
        Used for presorting_123-456 to presorted_123-456 and consolidating_234-567 to consolidated_234-567
        Returns: the name of the rolled back file
        """
        # TODO control error if rename fails
        rolledfname = ""
        if fname: # i.e. ../dir1/dir2/consolidating_123-456
            fname_split = os.path.split(fname) # ../dir1/dir2/  consolidating_123-456

            rname = fname_split[1].replace("ing", "ed") # consolidated_123-456
            rolledfname = os.path.join(fname_split[0], rname)
            os.rename(fname, rolledfname)
            # n_split = fname_split[1].split("_") # consolidating  123-456
            # prefix = n_split[-2] # consolidating
            # post_unique = n_split[-1] # 123-456
            # if prefix.endswith("ing"):
            #     roll_prefix = prefix.replace("ing", "ed") # consolidated
            #     rolledfname = self._rename_file(fname_split[0], fname_split[1], fname_split[0], roll_prefix + "_" + post_unique)

        return rolledfname

    def _get_presorted(self):
        """
        Gets a presorted file from de consolidation pool.
    
        If renaming fails the show must go on, may be a parallel consolidator got the file just before, so look for the next
        Returns: the name of the presorted file renamed to be consolidated (prefix consolidating_), empty string if renaming fails
        """
        # TODO control error if rename fails
        newfname = ""
        for fname in os.listdir(self.consolidation_pool_pathname):
            if fname.startswith(msg.PRESORTEDPFX): # get presorted files only, avoid files consolidating_
                newfname = self._rename_file(self.consolidation_pool_pathname, fname, self.consolidation_pool_pathname, msg.CONSOLIDATINGPFX)
                break

        return newfname


    def _get_consolidated(self):
        """
        Gets a consolidated file from de consolidation pool.
    
        If renaming fails the show must go on, may be a parallel consolidator got the file just before, so look for the next
        Returns: the name of the consolidated file renamed to be consolidated (prefix consolidating_), empty string if renaming fails
        """
        # TODO control error if rename fails
        newfname = ""
        for fname in os.listdir(self.consolidation_pool_pathname):
            if fname.startswith(msg.CONSOLIDATEDPFX): # get presorted files only, avoid files consolidating_
                newfname = self._rename_file(self.consolidation_pool_pathname, fname, self.consolidation_pool_pathname, msg.CONSOLIDATINGPFX)
                break

        return newfname


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
            oldfname = os.path.join(old_path, old_name)
            newpref = self._reprefix_file(old_name, new_prefix)
            newfname = os.path.join(new_path, newpref)
            os.rename(oldfname, newfname) # POSIX atomic operation
        except OSError as err:
            logging.error(f"Unexpected {err=}, {type(err)=}")
            newfname = ""

        return newfname


    def _reprefix_file(self, old_name, new_prefix):
        """
        Gets a file name (just a string) as <prefix>_<unique_id> and changes it to <new_prefix>_<unique_id>.
    
        Args:
            old_name: original name as <prefix>_<unique_id>
            new_prefix: new name as <new_prefix>_<unique_id>
        """
        unique_postfix = old_name.split("_")[-1]
        newpref = new_prefix + unique_postfix

        return newpref

   # TODO avoid repeated code
    def _create_consolidating_file(self):
        """
        Opens a file to store consolidated values.
    
        """
        f = None
        try:
            prefix = msg.CONSOLIDATINGPFX
            unique_postfix = str(uuid.uuid4())
    
            fname = os.path.join(self.consolidation_pool_pathname, prefix + unique_postfix)
            f = open(fname, 'w')
    
            logging.debug(f"New consolidating {fname=}")
        except Exception as e:
            logging.critical(f"Failed to create consolidating file {fname=}")
            # sys.exit()
        
        return f


    # TODO avoid repeated code -> use reprefix
    def _close_consolidating_file(self, f):
        """
        Closes a consolidating file.
    
        File name is changed from consolidating to consolidated
        """
        try:
            prefix = msg.CONSOLIDATEDPFX

            oldfname = f.name
            unique_postfix = oldfname.split("_")[-1]
    
            newfname = os.path.join(self.consolidation_pool_pathname, prefix + unique_postfix)
            f.close()
            os.rename(oldfname, newfname) # POSIX atomic operation
    
            logging.debug(f"New consolidated file {newfname=}")
        except Exception as e:
            logging.critical(f"Failed to close consolidating file {oldfname=}")
            sys.exit()


