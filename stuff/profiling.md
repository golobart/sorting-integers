This file just contains some stuff like tests and profilings.

_____

### executing

.\envs\sort-int\Scripts\activate  
cd .\gitlab\sorting-integers\src  
python .\main.py -if ..\data\in\numbers.txt -of ..\data\out\sorted_numbers.txt -n 10  
python test_sort.py  
  
bucket_average = 2**10  
python main_slicer.py -n 10000 -if ../data/in/numbers_1.txt -of pepepepe  
python main_presorter.py -n 10000 -if ../data/in/numbers_1.txt -of pepepepe  
  
bucket_average = 2**16  
python main_slicer.py -n 100000 -if ../data/in/numbers_30.txt -of pepepepe  
python main_presorter.py -n 100000 -if ../data/in/numbers_30.txt -of pepepepe  
python main_presorter.py -n 30000000 -if ../data/in/numbers_30.txt -of pepepepe  
python main_consolidator.py -n 100000 -if ../data/in/numbers_30.txt -of ../data/out/sorted100000.txt  
  
Times are for Lenovo ThinkPad T14 core i5
10 mins (100.000 biggest from 30.000.000)  
python main_serial.py -n 100000 -if ../data/in/numbers_30.txt -of ../data/out/numbers_30_100000_sorted.txt  
4 mins would improve with parallel consolidators (100.000 biggest from 30.000.000)  (6 min using heap_max)
python main_parallel.py -n 100000 -if ../data/in/numbers_30.txt -of ../data/out/numbers_30_100000_sorted.txt  
  
20 mins, enough with 1 consolidator (30.000.000 biggest from 100.000.000)  
python main_parallel.py -n 30000000 -if ../data/in/numbers_100.txt -of ../data/out/numbers_100_30000000_sorted.txt  

6 mins, enough with 1 consolidator (30.000.000 biggest from 50.000.000)  
python main_parallel.py -n 30000000 -if ../data/in/numbers_50.txt -of ../data/out/numbers_50_30000000_sorted.txt  

11 mins, enough with 1 consolidator (2.000.000 biggest from 100.000.000)  
python main_parallel.py -n 2000000 -if ../data/in/numbers_100.txt -of ../data/out/numbers_100_2000000_sorted.txt  

5 mins, enough with 1 consolidator (2.000.000 biggest from 50.000.000)  
python main_parallel.py -n 2000000 -if ../data/in/numbers_50.txt -of ../data/out/numbers_50_2000000_sorted.txt  

10 mins!!! (30.000.000 biggest from 50.000.000)  
 python .\main_parallel.py -n 30000000 -if ..\data\in\numbers_50.txt -of ..\data\out\numbers_50_30000000_sorted_heapmax.txt

15 mins (30.000.000 biggest from 100.000.000) (Linux sort takes 7 minutes ```sort -rn 100000000_nums.txt | head -30000000```)
 python .\main_parallel.py -n 30000000 -if ..\data\in\numbers_a100.txt -of ..\data\out\numbers_a100_30000000_sorted.txt

 16 mins (30.000.000 biggest from 100.000.000)
 python .\main_parallel.py -n 30000000 -if ..\data\in\numbers_a100.txt -of ..\data\out\numbers_a100_30000000_sorted2.txt

 25 mins??? (30.000.000 biggest from 100.000.000)
 python .\main_parallel.py -n 30000000 -if ..\data\in\numbers_a100.txt -of ..\data\out\numbers_a100_30000000_sorted_mergesort.txt
 
 28 mins (30.000.000 biggest from 100.000.000)
 python .\main_interleaced.py -n 30000000 -if ..\data\in\numbers_a100.txt -of ..\data\out\numbers_a100_30000000_sorted_mergesort.txt

Powershell -> ctrl-c process after more than 50 minuts running with full memory occupation and humunguous(tens of milions) number of Page Faults!!!
 Get-Content -Path ..\data\in\numbers_a100.txt | Sort-Object -Descending {[int]$_} | Select-Object -First 30000000 | Out-File -FilePath ..\data\out\numbers_a100_30000000_sorted_PowerShell.txt

### profiling:

python -m cProfile -o main.prof main.py -if ..\data\in\numbers.txt -of qq -n 10  
python -m cProfile  -s tottime main.py -if ..\data\in\numbers.txt -of qq -n 10  
python -m cProfile  -s cumtime main.py -if ..\data\in\numbers.txt -of qq -n 10
```
 --> python -m cProfile  -s cumtime main.py -if ..\data\in\numbers.txt -of qq -n 10000000

         8998555 function calls (8998002 primitive calls) in 216.432 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     27/1    0.000    0.000  216.432  216.432 {built-in method builtins.exec}
        1    0.002    0.002  216.432  216.432 main.py:3(<module>)
        1    0.000    0.000  216.365  216.365 main.py:12(main)
        1    5.414    5.414  216.314  216.314 py_array_insort.py:31(select_nbig)
   990154    1.780    0.000  205.229    0.000 py_array_insort.py:88(_try_to_store)
   990154    1.162    0.000  203.450    0.000 py_array_insort.py:137(_store_number)
   990139  202.288    0.000  202.288    0.000 {method 'insert' of 'array.array' objects}
  1000000    1.425    0.000    2.328    0.000 base_selector.py:94(_check_line)
   999994    2.217    0.000    2.217    0.000 {built-in method _bisect.bisect_right}
  1000001    0.791    0.000    0.839    0.000 base_selector.py:78(_input_file_gen)
  1000000    0.529    0.000    0.529    0.000 {method 'isdigit' of 'str' objects}
  1001371    0.375    0.000    0.375    0.000 {method 'rstrip' of 'str' objects}
1002178/1002060    0.271    0.000    0.271    0.000 {built-in method builtins.len}
     35/6    0.001    0.000    0.098    0.016 <frozen importlib._bootstrap>:1002(_find_and_load)
     35/6    0.000    0.000    0.097    0.016 <frozen importlib._bootstrap>:967(_find_and_load_unlocked)
     33/8    0.000    0.000    0.090    0.011 <frozen importlib._bootstrap>:659(_load_unlocked)
```

```
  --> python -m cProfile  -s tottime main.py -if ..\data\in\numbers.txt -of qq -n 10000000

         8998555 function calls (8998002 primitive calls) in 170.356 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   990139  159.152    0.000  159.152    0.000 {method 'insert' of 'array.array' objects}
        1    4.221    4.221  170.215  170.215 py_array_insort.py:31(select_nbig)
   999994    1.748    0.000    1.748    0.000 {built-in method _bisect.bisect_right}
   990154    1.389    0.000  161.460    0.000 py_array_insort.py:88(_try_to_store)
  1000000    1.158    0.000    1.879    0.000 base_selector.py:94(_check_line)
   990154    0.919    0.000  160.071    0.000 py_array_insort.py:137(_store_number)
  1000001    0.622    0.000    0.680    0.000 base_selector.py:78(_input_file_gen)
  1000000    0.415    0.000    0.415    0.000 {method 'isdigit' of 'str' objects}
  1001371    0.306    0.000    0.306    0.000 {method 'rstrip' of 'str' objects}
1002178/1002060    0.214    0.000    0.214    0.000 {built-in method builtins.len}
     1198    0.036    0.000    0.036    0.000 {built-in method _codecs.charmap_decode}
        2    0.029    0.014    0.029    0.014 {built-in method io.open}
      162    0.021    0.000    0.021    0.000 {built-in method nt.stat}
       26    0.020    0.001    0.020    0.001 {built-in method io.open_code}
       34    0.012    0.000    0.012    0.000 {method 'write' of '_io.TextIOWrapper' objects}
        2    0.010    0.005    0.010    0.005 {built-in method _imp.create_dynamic}
      422    0.007    0.000    0.011    0.000 <frozen importlib._bootstrap_external>:91(_path_join)
       26    0.005    0.000    0.005    0.000 {built-in method marshal.loads}
     1198    0.005    0.000    0.040    0.000 cp1252.py:22(decode)
  102/100    0.004    0.000    0.017    0.000 {built-in method builtins.__build_class__}
  ```