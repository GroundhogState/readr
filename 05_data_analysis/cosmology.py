"""
cosmological functions -- defined this way instead of using solely astropy.cosmology,
to take into account two different redshifts going into the luminosity distance
"""

import numpy as np
import astropy.cosmology as cosmo

def Comoving_Distance(z, Omega_M, Omega_L, w_o, w_a):

    wcdm = cosmo.wCDM(H0=70., Om0=Omega_M, Ode0=Omega_L, w0=w_o)

    return np.array(wcdm.comoving_distance(z))


def Luminosity_Distance(z_hel, z_cmb, Omega_M, Omega_L, w_o, w_a):

    D_c = Comoving_Distance(z_cmb, Omega_M, Omega_L, w_o, w_a)

    return D_c * (1+z_hel)


def distance_modulus(z_hel, z_cmb, Omega_M, Omega_L, w_o, w_a):

    D_L = Luminosity_Distance(z_hel, z_cmb, Omega_M, Omega_L, w_o, w_a)

    mu = 25 + 5*np.log10(D_L)

    return mu
