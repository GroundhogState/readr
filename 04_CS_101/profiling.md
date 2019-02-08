# Key profiling points
## cProfile
- Standard library module for profiling code.
- Can profile from a script like:
```
import cProfile
import linear_systems
cProfile.run("linear_systems.main()")
```
or on the command line with:
```
$ python3 -m cProfile linear_systems
```
- This will produce a flat profile of functions and function calls:

```
         492457 function calls in 12.500 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   12.500   12.500 <string>:1(<module>)
        9    0.000    0.000    0.000    0.000 _bootlocale.py:23(getpreferredencoding)
        9    0.000    0.000    0.000    0.000 codecs.py:185(__init__)
        9    0.000    0.000    9.008    1.001 linear_systems_unoptimised.py:102(get_scalefactor)
        9    0.054    0.006    0.223    0.025 linear_systems_unoptimised.py:107(save_matrices)
        1    0.001    0.001   12.358   12.358 linear_systems_unoptimised.py:125(vec_func_2)
        1    0.000    0.000    0.000    0.000 linear_systems_unoptimised.py:129(<listcomp>)
        1    0.000    0.000   12.500   12.500 linear_systems_unoptimised.py:143(main)
        2    0.011    0.005    0.073    0.037 linear_systems_unoptimised.py:16(gen_matrix)
        2    0.000    0.000    0.000    0.000 linear_systems_unoptimised.py:18(<listcomp>)
      200    0.001    0.000    0.001    0.000 linear_systems_unoptimised.py:20(<listcomp>)
        9    0.001    0.000    0.001    0.000 linear_systems_unoptimised.py:35(one_divide_vec)
     4009    0.063    0.000    0.064    0.000 linear_systems_unoptimised.py:42(dot)
       10    0.001    0.000    0.001    0.000 linear_systems_unoptimised.py:52(axpy)
        9    0.058    0.006    0.058    0.006 linear_systems_unoptimised.py:59(matvec)
        9    0.000    0.000    0.000    0.000 linear_systems_unoptimised.py:62(<listcomp>)
        9    3.002    0.334    3.031    0.337 linear_systems_unoptimised.py:69(matmul)
        9    0.000    0.000    0.000    0.000 linear_systems_unoptimised.py:73(<listcomp>)
        2    0.000    0.000    0.002    0.001 linear_systems_unoptimised.py:8(gen_vector)
        9    0.035    0.004    0.035    0.004 linear_systems_unoptimised.py:86(scale_matrix)
       40    0.003    0.000    0.066    0.002 linear_systems_unoptimised.py:94(vec_func_1)
    20200    0.023    0.000    0.053    0.000 random.py:173(randrange)
    20200    0.010    0.000    0.063    0.000 random.py:217(randint)
    20200    0.022    0.000    0.030    0.000 random.py:223(_randbelow)
        9    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        1    0.000    0.000   12.500   12.500 {built-in method builtins.exec}
    97736    0.011    0.000    0.011    0.000 {built-in method builtins.len}
        9    0.001    0.000    0.001    0.000 {built-in method io.open}
        9    9.007    1.001    9.007    1.001 {built-in method time.sleep}
    96100    0.019    0.000    0.019    0.000 {method 'append' of 'list' objects}
    20200    0.002    0.000    0.002    0.000 {method 'bit_length' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    90900    0.140    0.000    0.140    0.000 {method 'format' of 'str' objects}
    30706    0.006    0.000    0.006    0.000 {method 'getrandbits' of '_random.Random' objects}
    91827    0.028    0.000    0.028    0.000 {method 'write' of '_io.TextIOWrapper' objects}
```

By default, the profile is ordered by function name, but we can sort it by, e.g. total time via the
`-s` option on the command line:

```
python3 -m cProfile -s tottime linear_systems
```

`-s` can sort by any of the column headings. 
- Profiles can produce a lot of output, so it's best to either pipe through `less` or redirect the
  output to a file via the `-o filename.dat` option (alternatively, we can pass a filename as the second
  argument to `cProfile.run("linear_systems.main()", "filename.dat")` from a script).

## Microbenchmarking (aka print-statement profiling)
- cProfile is very powerful for finding which *functions* are taking a lot of time, but doesn't help
  much with finding the bottlenecks *within* a function. For this, we can use good old fashioned
  print-statements (microbenchmarking, in more formal terminology).
- The `time` module contains a bunch of useful functions for retrieving and manipulating the time.
- The simplest way to get some microbenchmarks is with the `time.perf_counter()` function, which returns
  the current "processor time" (in seconds) as a floating point number. Crucially, this function is
  different from `time.clock()` and friends in that `time.perf_counter()` is defined such that the
  difference between two time points is meaningful (which is exactly what we want).
- The simplest way to use this functionality is to enclose a section of code in time-stamps like so:

```
import time

start = time.perf_counter()
do_stuff()
end = time.perf_counter()

elapsed = end - start
print("do_stuff finished in {} s".format(elapsed))
```

You can have as many sections like this in a module as necessary, provided none of the variable names
clash.
