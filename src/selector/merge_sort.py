import logging
import array as arr
import bisect
import time

from selector.base_selector import Selector


class MergeSort(Selector):
    """
    Selector of top numbers based on MergeSort sorting algorithm.

    """
    def __init__(self, args, conf):
        """
        Initializes topn store as a Python array at its max capacity (args.nbig).
    
        Has to leave self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            args: command line arguments.
            conf: General section of config.ini file
        """
        super(MergeSort, self).__init__(args, conf)
                                          

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

        # arr = [1, 12, 9, 5, 6, 10]
        # heapSort(arr)
        # n = len(arr)
        # print("Sorted array is")
        # for i in range(n):
        #     print("%d " % arr[i], end='')

        for elem in iter_numbers:
            self.line_cnt += 1
            self.topn.append(elem)
        
        self.mergeSort(self.topn)
        self.topn.reverse()
        self._store_array_report()


    def mergeSort(self,array):
        if len(array) > 1:
    
            #  r is the point where the array is divided into two subarrays
            r = len(array)//2
            L = array[:r]
            M = array[r:]
    
            # Sort the two halves
            self.mergeSort(L)
            self.mergeSort(M)
    
            i = j = k = 0
    
            # Until we reach either end of either L or M, pick larger among
            # elements L and M and place them in the correct position at A[p..r]
            while i < len(L) and j < len(M):
                if L[i] < M[j]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = M[j]
                    j += 1
                k += 1
    
            # When we run out of elements in either L or M,
            # pick up the remaining elements and put in A[p..r]
            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1
    
            while j < len(M):
                array[k] = M[j]
                j += 1
                k += 1

