import numpy as np
import matplotlib.pyplot as plt

# 0. write a loop over integers from 0 to 100 (inclusive) that
#   a) appends to x_list if divisible by 5, and
#   b) prints 'square' if is a square number

x_list = []
for ...

# 1. make an array of integers divisible by 5 from 1 and 100 using numpy

x_arr = np.(...)

# i.e. the below should evaluate to True
# print 'checkpoint: ', np.all(x_arr == np.array(x_list))

# 2. define a new array y_arr as the sine of (x_arr/10), and plot it

y_arr = ...

# 3. define a new array by slicing y_arr that only every third value

y_sel = y_arr[...]

# 4. define a function that returns the square of x+5. we will check the
# outputs of this function on the array defined in 3
#
def my_function(x):
    x += 5
    ret = ...
    return ret

# let's check on x_sel
print my_function(x_sel)

# 6. regenerate your plot above: what happens to it, and why? how would you
# change the function definition to avoid this?
