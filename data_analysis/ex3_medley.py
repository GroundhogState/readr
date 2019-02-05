import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt

# 1. simulate a data set with an exponential relation i.e.
# f(x) = A*e**x + B
# a) first set up an x-array, and compute f(x)
# b) generate some noise from a normal distribution, and add this to
# your data (y_data)
# c) generate noise again from the same distribution, and make this
# your error data (y_err)
# d) plot the data with errorbars

def my_function(x, A, B):
    ...
    ret = ...
    return ret

x_data = ...
y_data = ...
y_err = ...

# 2. save this data to a .txt file using np.savext.
# swap it with someone else who has done the same

# 3. now try fit for parameters, from first principles, using a grid
#   a) first define a chi-squared function chisq(A,B)
#   b) set up an array in A and B (hint: np.meshgrid may help)
#   c) plot contour plots, and adjust your array (hint: plt.contour may help)
#   d) appreciate how tedious/slow/hard this might be when
#   you have >2 variables, your function is more complicated,
#   your data is messier, ...

def chisq(A,B):
    ...
    ret = ...
    return ret

# 4. now try using MCMC:
#   a) set up your lnlike, lnprob functions using the same
#   chisq function as in 3a
#   b) play with parameters in the fitter
