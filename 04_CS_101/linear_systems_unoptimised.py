#!/usr/bin/python3

import numpy as np
import scipy.special
import random
import time

def gen_vector(size):
    """ Generates a random vector of the specified size."""
    ret = []
    for _ in range(size):
        ret.append(random.randint(0, 20))
    
    return(ret)

def gen_matrix(size):
    """ Generates a random size x size matrix."""
    ret = [[] for _ in range(size)]
    for i in range(size):
        ret[i] = [[] for _ in range(size)]

        for j in range(size):
            ret[i][j] = random.randint(0, 20)
    
    return(ret)

def vecnorm(x):
    """ Calculates the norm (magnitude) of a vector x."""
    norm = 0
    for i in range(len(x)):
        norm += x[i]**2

    return(norm)

def one_divide_vec(x):
    """ Calculates the vector 1/x = [1/x_1, 1/x_2, 1/x_3] """
    ret = []
    for element in x:
        ret.append(1.0/element)
    return(ret)

def dot(x, y):
    """ Calculates the dot product of two vectors x and y."""
    ret = 0

    # Question: is this slower than using an iterator or list comprehension?
    for i in range(len(x)):
        ret += x[i] * y[i]

    return(ret)

def axpy(a, x, y):
    """ Function to compute y = a*x + y"""
    ret = []
    for i in range(len(x)):
        ret.append(y[i] + a*x[i])
    return(ret)

def matvec(A, x):
    """ Computes the matrix-vector product A*x"""

    ret = [0 for _ in x]
    for i in range(len(x)):
        # Iterate over the i'th row of A
        for j in range(len(A[i])):
            ret[i] += A[i][j]*x[j]
    return(ret)

def matmul(A, B):
    """ Computes the matrix-matrix product A*B for square matrices"""
    # Question: Can this function handle matrices of every size? Think about the maths, 
    # write some tests, and then modify the function to work in all cases
    ret = [[] for _ in range(len(A))]
    for row in ret:
        for _ in range(len(B[0])):
            row.append(0) # Fill the row with zeros
    
    # Now do the matrix multiplication
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                ret[i][j] += A[i][k] * B[k][j]

    return(ret)

def scale_matrix(A, c):
    """ Computes the matrix-scalar product A*c"""
    ret = A # Note: we need to make a copy here because of the way Python handles variables in memory
    for i in range(len(ret)):
        for j in range(len(ret[i])):
            ret[i][j] *= c
    return(ret)

def vec_func_1(x, y, z, const):
    """ Arbitrary vector function. Computes ret = (z + (x dot y))/const."""

    ret = []
    for i in range(len(z)):
        ret.append((z[i] + dot(x, y))/const) #Task: unit tests should consider: len(x) != len(y) etc, const == 0
    return(ret)

def get_scalefactor(z):
    """ Arbitrary expensive function to calculate the scaling factor in vec_func_2"""
    time.sleep(1) # Don't remove this, it's here to approximate an expensive function
    return(scipy.special.erf(z)) # Bessel function of the first kind

def save_matrices(u, T, filename):
    """ Saves the vector u and matrix T from vec_func_2 to a file"""
    
    # Open our file for writing. It will automatically be closed once we're done
    with open(filename, 'w') as ofp:
        # Write out the vector first
        ofp.write("# vector u:\n[ ")
        for element in u:
            ofp.write("{}  ".format(element))
        ofp.write("]\n# matrix T:\n[[")
            
        # Now write out the matrix
        for row in T:
            for element in row:
                ofp.write("{}  ".format(element))
            ofp.write("]\n")
        ofp.write("]")

def vec_func_2(A, B, x, num_iter):
    """ Arbitrary iterative vector function. There are huge optimisation opportunities here, so 
        profile it carefully."""
    ret = 0
    u_old = [0 for _ in range(len(x))]

    for b in range(num_iter):
        for a in range(num_iter):

            scalefactor = get_scalefactor(a/20.0)

            T = scale_matrix(matmul(A, B), scalefactor) 
            u = one_divide_vec(axpy(b, x, matvec(T, x)))
            ret += dot(u_old, u)
            u_old = u
            save_matrices(u, T, "vec_func_2.txt")
    return(ret)

def main():
    # Do some linear alegbra
    size = 100
    x = gen_vector(size)
    y = gen_vector(size)
    z = axpy(0.5, x, y)
    A = gen_matrix(size)
    B = gen_matrix(size)

    for i in range(10, 50):
        len(vec_func_1(x, y, z, i))

    vec_func_2(A, B, x, 3)


if __name__ == "__main__":
    main()
