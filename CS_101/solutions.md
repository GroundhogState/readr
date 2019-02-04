# Emily's Software 101

## Optimisations solutions
### `dot(x, y)` - dot product
- This is about as fast as you can get without going to numpy
- It is slightly faster for very large vectors to do:

```
for x_it, y_it in zip(x, y):
    ret += x_it * y_it
```

rather than the naive:

```
for i in range(len(i)):
    ret += x[i] * y[i]
```

But this is not a huge improvement (< 10%).

- Is it worth adding in a check for x, y = zero vector?
    * No, since that requires checking all the elements of each vector

- Unit tests should check: 
    * len(x) != len(y) (so need to add an assertion to catch this) 
    * Invalid values (e.g. vectors have the wrong type (like strings) in them). Add an exception
      handler.

### `axpy` - sanity checks
- `axpy` currently doesn't check to see if the scalar factor a is nonzero. Obviously we can skip the 
multiplications and additions and simply return y if a = 0. This will save some time in the inner loop
of `vec_func_2` where the loop-variable is zero. This is a small-optimisation, but can be important if
we call this lots of times for large vectors.

### `scale_matrix` and `matmul` - Working memory and copying data structures
- I don't think we can do things differently in python (it doesn't really have an equivalent of call 
  by reference semantics), but this is a good opportunity to talk about memory management.
- For large matrices and vectors, it is often faster to modify them in-place to avoid allocating too
  much memory for the result matrix/vector. Not only does this save on memory usage (potentially 
  huge amounts for real scientific code), it can also dramatically reduce run-time, as allocating heap
  memory can take a lot of time if it's done inside a tight loop.
- Similarly, `matmul` and similar subroutines require some "working memory", in this case to hold the 
  product of the two matrices. Currently, it is allocated *inside* the subroutine, which means we'll be 
  re-allocating memory extremely frequently inside the inner-loop of `vec_func_2`. This is basically 
  unavoidable in Python, but in C or Fortran we can allocate working memory *outside* the loop and pass
  in a pointer to that memory so it only gets `alloc`'d and `free`'d once.

### `vec_func_1` - dealing with loop invariants
- This function returns a list of the same size as x, y, z. Is it faster to pre-allocate the returned
  list? Yes, for N = 10,000 we get an improvement of around 4s (from 65s to 61s for around 6% gain).
- The dot-product (x, y) is loop-invariant, so calculate it once, before entering the loop. This reduces
  the run-time for N = 10,000 from 66s to 0.353s.
    * This is the big one I want the students to find here.

### `vec_func_2` - I/O and caching frequently-used calculations
There's a couple of really big optimisations to be had here:
- The biggest one is when calculating the scaling factor. This is an artifically expensive function 
(I just added a sleep() call to the function body), but expensive, frequently-called functions are 
very common in real code. Sometimes you can optimise the algorithm or swap out the function for a 
faster version from some external library, but some functions are just inherently expensive. In this 
case, we can cache the results of frequently-called functions to speed up execution, like so:
```
function_cache = {} # Empty dict
if (arg1, arg2) in function_cache: # Check if we've already stored the value corresponding to our function arguments
    value = function_cache[(arg1, arg2)] # Just grab the value from the cache, sometimes much faster than re-calculating
else:
    value = expensive_function(arg1, arg2)
    function_cache[(arg1, arg2)] = value # Store our recently computed value with some key based on the arguments
```

Caching basically trades memory usage for increased effeciency. In order for this optimisation to be 
useful, we generally require three conditions:
    1) The function must take longer to calculate than it does to fetch the results from the cache.
    2) The function must be frequently-called with the same arguments. Caching is only useful if you re-use the 
    stored values multiple times.
    3) The function must have a relatively simple return type (e.g. an integer or a float) and have a relatively small
    range of argument values (e.g. the scale-factor in `vec_func_2` has only num_iter possible inputs)

Applying this optimisation to `vec_func_2` dramatically decreases the run-time once we've run through the inner-loop once
and stored all possible values of the scaling factor. Once we've cached the results it finishes execution almost instantly,
compared to taking several minutes without the caching.

- The second major optimisation is the progress-write in the inner loop: we save a matrix and vector to a file after every
iteration. Disk I/O is **really** slow, so we want to not do this inside tight-loops. If all we want is to save the final 
matrix, then we can hoist the save_matrices subroutine outside the loop and only do it once we've finished all the 
calculations. Sometimes we do want to save the intermediate steps as we go so we can resume part-way through a calculation
which has halted prematurely. This is called *checkpointing* and most real HPC software requires at least some form of saving
incremental progress (indeed, some supercomputer administrators will *require* you to implement checkpoints before you can use 
their clusters). If we want checkpoints, then it is often unnecessary to save after every single iteration. Instead, we can 
save after every 100th iteration, for example, via:
```
if (a % 100 == 0):
    save_matrices(...)
```

- As a general rule, I/O is extremely slow compared to other operations (even for solid-state drives it's still >100x slower 
than memory accesses), so you want to do as little of it as possible and delay it until as late as possible.

- In addition to these, we have a matrix-multiply which can be hoisted outside the loop. Also, `one_divide_vec` doesn't properly
handle zero vectors for input, so will need to be fixed (this isn't strictly a real operation in linear algebra, so it's somewhat
arbitrary what "fix" means).
