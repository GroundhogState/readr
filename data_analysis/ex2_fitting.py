import numpy as np
from scipy import curve_fit

datafile = 'R11_table2.txt'

cepheid_data = np.genfromtxt(datafile,skip_header=18,
                             usecols=(0,4,5,6,7,11,12),
                             names='galaxy,P,V-I,m_H,err_m_H,met,rej',
                             dtype='S8,f8,f8,f8,f8,f8,f8'
                             )

# 0. load the cepheid data in alternative ways using np.loadtxt and/or pandas

"""
you are given that the Leavitt law relates the period, luminosity, metallicity
of Cepheid variables in a given galaxy i by
m_W,i = a*[log10(P)-1] + b*(metallicity - 8.89) + c + mu_i
where:
    - mu_i is a constant for each galaxy - basically it is a proxy for distance,
or distance modulus; larger mu means further away
    - m_W = m_H - 0.410*(V-I) is a colour/dust-corrected magnitude; smaller m
    means brighter
"""

# 1. make some plots, showing each galaxy with a different colour and/or symbol
#   a) what do the rejection flags mean? i.e. why are these stars rejected? note
#      1 and 2 are separate flags
#   b) does brightness depend primarily on period, or on metallicity?

# 2. using just cepheids in ngc 4258, obtain a rough estimate for coefficients
# a and/or b (as appropriate/possible) using:
#   a) np.polyfit
#   b) scipy.curve_fit
# optional: plot residuals for your fits in 2. as you see fit (hint: what might these
# residuals depend on?)

# 3. now repeat 2b), taking into account errors in m_W - you may assume
# err_m_W = err_m_H
# how do the results and errors change?

""" EXTENSIONS """

# 4. now try to fit for mu_4536 and mu_3370, assuming mu_4258 = 29.404
# hint: it may be easier to define c' := c + mu_4258, and fit for e.g. mu_4258-mu_4536
# optional: try to find both simultaneously, rather than one at a time. how do
# your results differ?

# 5. extension: try to use MCMC to fit for a, b, c

# 6. extension: what happens to the fit if you remove the offset terms in the
# Leavitt law? i.e.
# m_W,i = a2*log10(P) + b2*metallicity + c2 + mu_i
