Sorter-Selector system has been developed and tested under Windows 10 and Python 3.9.7.  
The development has also been tested in Fedora 35 and Python 3.10.4.  
You don't need to install any additional module or library to run it.

The Sorter-Selector is a 3 steps strategy:
1. Slicer, takes the input file and divides it in smaller files of n lines (slice)
2. Presorter, Sorts each slice
3. Consolidator, processes sorted slices in pairs selecting the n biggests values from both files

To run Sorter-Selector in serial mode (1 then 2 then 3):
```
$ cd sorting-integers/src
$ python main_serial.py -n <number> -if <input file>> -of <output file>
```

To run Sorter-Selector in interleaced mode (1, 2 and 3 simultaneously):
```
$ cd sorting-integers/src
$ python main_interleaced.py -n <number> -if <input file>> -of <output file>
```

To run Sorter-Selector in parallel mode (1, 2, 2, 2 and 3 simultaneously) 3 presorters in parallel:
```
$ cd sorting-integers/src
$ python main_parallel.py -n <number> -if <input file>> -of <output file>
```

Note: Slicer and Consolidator have not been parallelized.

Some tests has also been provided:
```
$ cd sorting-integers/src
$ python test_sort.py
```
Note: the py_array_preall test fails unless you create the ../data/in/init_store.txt file, to create 
this file use src/gen_file.py (edit it and uncomment the right lines and then execute ```$ python gen_file.py```).


That should be all. 

Notes:  
You can also run the raw Selector part of the project (look at config.ini file for allowed Selectors):
```
$ cd sorting-integers/src
$ python main.py -n <number> -if <input file>> -of <output file>
```

Selector objects do just the sort part of the process.
The provided selectors implement the insort sorting algorithm (with few variations)

To write more selectors (i.e. for merge sort or quick sort algorithms):
- Use Selector as a base class (base_selector.py)
- Modify factory acordingly (factory.py)
- Include the new value for store_top parameter in the config.ini file


How to improve this project:
- Try other sorting algorithms like merge sort, quick sort, shell sort or any other
- Parallelize the consolidation part (this is almost done but lacks of some details)
- Containerize each phase, make a Docker image for each of Slicer, Presorter and Consolidator
- Deploy the images in Kubernetes as Pods
- Try a new sorting strategy: bucketizer-presorter-consolidator

Time and space complexity:
- Slicer  
Space complexity is N because for N input elements it takes N additional space  
Time complexity is also N, for N input elements performs N operations (checks validity and stores to file)

- Presorter  
This phase is a combination of a one step bucketization plus sorting each bucket (fixed size buckets).  
If I'm not wrong this makes the time complexity N, because whatever the sorting algorithm you use it sorts
k buckets of fixed size so if you doubles the number of buckets (or elements) you just doubles the number
of operations.  
Space complexity is also N because the one step bucketization uses N more space and the inner Selector uses
also N

- Consolidator  
It creates a file of size k from two files of k elems each, and because it just works in pairs, space
complexity is 1.  
Time complexity is N, for each slice you add, you just need one more consolidation.  
