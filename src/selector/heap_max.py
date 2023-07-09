import logging
import array as arr
import bisect
import time

from selector.base_selector import Selector


class HeapMax(Selector):
    """
    Selector of top numbers based on Heap Max sorting algorithm.

    """
    def __init__(self, args, conf):
        """
        Initializes topn store as a Python array at its max capacity (args.nbig).
    
        Has to leave self.topn populated with the sorted largest numbers (self.nbig numbers).
        Args:
            args: command line arguments.
            conf: General section of config.ini file
        """
        super(HeapMax, self).__init__(args, conf)
        
                                  

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
        
        self.heapSort(self.topn)
        self.topn.reverse()
        self._store_array_report()


    def heapify(self, arr, n, i):
        # Find largest among root and children
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
    
        if l < n and arr[i] < arr[l]:
            largest = l
    
        if r < n and arr[largest] < arr[r]:
            largest = r
    
        # If root is not largest, swap with largest and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)
  
  
    def heapSort(self, arr):
        n = len(arr)
    
        # Build max heap
        for i in range(n//2, -1, -1):
            self.heapify(arr, n, i)
    
        for i in range(n-1, 0, -1):
            # Swap
            arr[i], arr[0] = arr[0], arr[i]
    
            # Heapify root element
            self.heapify(arr, i, 0)
