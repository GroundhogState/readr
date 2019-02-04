#!/usr/bin/python3

import linear_systems_unoptimised as linear
import time

if __name__ == "__main__":
    
    start = time.perf_counter()
    linear.main()
    end = time.perf_counter()
    elapsed = end - start
    print("Program finished in {}s".format(elapsed))
