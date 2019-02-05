# Miscellaneous stuff you should know
## Python specific
- Learn the innards of Python:
    * How are lists actually implemented?
    * How are dicts implemented?
    * What actually happens when you run a script?
    * What is bytecode?
    * Why are there so many different interpreters?
    * How can you call C or Fortran code from python?
- Read the [numpy](https://github.com/numpy/numpy) and [scipy](https://github.com/scipy/scipy) source 
  codes to see how they implement functions you commonly use (the source will probably be a mix of 
  python and C).
- Try re-implementing the functions from numpy or scipy yourself. Compare the performance and semantics 
  to the library versions and try to figure out why they're different (again, read the source code).
- Give [Cython](https://cython.org/) a go. Cython is an optimising compiler for python that's kind of a
  python/C hybrid. It can really improve code execution time (although not as much as writing in plain C
  from the get-go).

## General CS
- Use an IDE/advanced code editor of some kind; they really help productivity and handle a lot of the 
  trivial stuff in programming (think of an IDE as being like a word-processor for code). Jupyter and 
  Anaconda will become more of a hindrance than a help as you get more proficient at programming). 
  There's a whole bunch of IDEs out there, so try some and pick one that you like (I quite like
  [Microsoft VS Code](https://code.visualstudio.com/))
- Know about operating systems and how to get the most out of them
    * Learn Linux/UNIX: this is what's installed on almost all clusters and servers, so you should know
      how to use them effectively
    * Know how to use command-line tools (e.g. GNU coreutils), as well as scripting (Bash or Powershell)
    * Windows is actually not very useful in scientific computing
- Learn a compiled language (particularly C, C++ and Fortran) - this will teach you a lot about software
  and how computers work (particularly memory and pointers)
- Learn how to use your compiler effectively. This includes writing code so it's easy to optimise,
  knowing when the compiler is smarter than you (almost always) and how to write code to effectively
  utilise CPU/hardware
    * Super important for numerical work: know the difference between row-major and column-major
      ordering for multidimensional arrays (matrices) and which one your language uses (C uses
      row-major, Fortran uses column-major).
- Learn how to use memory properly, particularly when to pass by value vs when to pass by reference.
    * Navigating caches and cache-coherency is critically important for high-performance code
- Hardware is important - every computational scientist should at least know the basics of CPU
  architecture (including how to find out what your machine is running on), memory models and I/O.
    * Have a rough understanding of how long different operations (e.g. cache hits, memory fetches,
      disk I/O) take to execute. 
      [Here's a good chart](http://ithare.com/infographics-operation-costs-in-cpu-clock-cycles/)
    * Also need to know about things like branch-prediction, speculative execution, 
      caching (really important), memory transfer rates, optimal arithmetic intensity (ratio of
      arithmetic operations to memory accesses).
    * For that matter, you should know how to determine whether your code is compute bound vs memory
      bound vs I/O bound and what the implications of that are (plus how to fix that for your specific
      hardware and OS)
- Know the basics of algorithms and data structures, as well as how they're implemented. The basics are:
    * computational complexity (big-O notation),
    * recursion,
    * searching,
    * sorting,
    * arrays, 
    * linked-lists, 
    * trees, 
    * associative arrays/hash tables, 
    * Threads, concurrency and asynchronous operations

- "Algorithms and Data Structures with Python" by Lee and Hubbard is a good starter text. Also check out
  "Algorithms and Data Structures in C" by Noel Kalicharan - it's super important to learn how to
  implement this stuff in C

- Read other people's code: great novelists read a variety of books, great programmers read a variety of
  code

- It's important to develop and intuition for when to write code yourself vs when to use a library. The
  general rule is "don't reinvent the wheel, unless you think you can do it better". Re-writing small
  functions can be fine (if it's going to take less time to write it yourself than to integrate a
  library), but think very carefully before trying to re-implement, say, a linear algebra library.

- Coding takes practice. You can pick up stuff as you go, but if you want to get really good it will
  require a bit of extra homework.

- Ergonomics is important! As a PhD student, your work depends crucially on being able to type, so RSI
  can **really** mess up your life. Get a good ergonomic setup as soon as possible (your university
  should be able to help with this).
