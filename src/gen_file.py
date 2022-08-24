#!/usr/bin/env python3

from random import seed
from random import randint
import time

def main():
    # generate random integer values
    seed(int(time.time()))

	# ----- Generate random file to sort
    f = open("../data/in/numbers_01.txt", "w")
    
    for _ in range(100000):
        value = randint(-1, 2**64)
        f.writelines(str(value) + "\n")
    
    f.close()
	# -----
    
    # ----- Generate 0s for initialization of py_array_preall test
    # f = open("../data/in/init_store.txt", "w")
    
    # for _ in range(30000001):
    # 	f.writelines("0\n")
    
    # f.close()
	# -----


if __name__ == "__main__":
    main()


