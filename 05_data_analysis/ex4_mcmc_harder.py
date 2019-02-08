import os
import datetime

import numpy as np
import emcee
from chainconsumer import ChainConsumer

from cosmology import distance_modulus

from optparse import OptionParser

""" simplified version of some cosmology-fitting code I had """

def lnlike(theta, z_hel, z_cmb, mb, x1, color, thirdvar, Ceta, sigma, model):
    if model.startswith('wCDM'):
        my_Om0, my_w0, alpha, beta, M_1_B, Delta_M = theta
    else:
        my_Om0, alpha, beta, M_1_B, Delta_M = theta
        my_w0 = -1

    N = len(mb)
    # observed distance modulus
    mu_obs = mb - (M_1_B - alpha * x1 + beta * color)
    # model distance modulus
    mu_theory = np.zeros(N)
    for j in range(N):
        mu_theory[j] = distance_modulus(zhel[j], zcmb[j], my_Om0, (1.0-my_Om0), my_w0, 0.0)
        if thirdvar[j] > 10:
            mu_theory[j] = mu_theory[j] + Delta_M

    dmu = #TODO

    # simple diagonal errors
    Cmu = np.zeros((N,N))
    for i in range(N):
        Cmu[i, i] += sigma[i][0]**2 + sigma[i][1]**2 + sigma[i][2]**2

    # the below involves inverting a matrix, which can lead to problems
    # if it doesn't work, see if you can define a chisq with only diagonal
    # errors from sigma only
    A = A_fn(alpha,beta,N)
    Cmu += A.dot(Ceta.dot(A.T))

    Cinv = np.linalg.pinv(Cmu)

    chisq = #TODO

    ## calculate and store parameters and chi^2 values
    with open(chains + '/params.txt', 'a') as f:
        if model.startswith('wCDM'):
            f.write(','.join([str(x) for x in [my_Om0, my_w0, alpha, beta, M_1_B, Delta_M]]) + '\n')
        else:
            f.write(','.join([str(x) for x in [my_Om0, alpha, beta, M_1_B, Delta_M]]) + '\n')
    with open(chains + '/chisq.txt', 'a') as f2:
        f2.write(str(chisq) + '\n')

    lnlike = -0.5 * chisq
    return lnlike

# gaussian prior on Omega_M~N(0.3,0.01)
def prior_Om(Om):
    return np.exp(-(Om-0.3)**2/(2*0.01**2))

def lnprob(theta, zhel, zcmb, mb, x1, color, thirdvar, Ceta, sigma, model):

    my_Om0 = theta[0]

    lnprior = 0
    if model == 'wCDMprior':
        p = prior_Om(my_Om0)
        if p < 1e-10:
            return -np.inf

        lnprior = np.log(p)
    if  0 < my_Om0 < 1.5:
        ret = lnprior + lnlike(theta, zhel, zcmb, mb, x1, color, thirdvar, Ceta, sigma, model)
        print ret
        return ret
    else:
        return -np.inf

def load_data():
    zhel = data[:,0]
    zcmb = data[:,1]
    mb = data[:,2]
    x1 = data[:,3]
    color = data[:,4]
    thirdvar = data[:,5]
    return zhel, zcmb, mb, x1, color, thirdvar

# function to very approximately estimate covariance matrix: you
# can use this without understanding the astronomy behind it
def covmat_tridiagonal(data):
    n = len(data)
    C = np.zeros((3*n,3*n))
    for i in range(n):
        cov=np.zeros((3,3))
        cov[0,0]=data['dmb'][i]**2.
        cov[1,1]=data['dx1'][i]**2.
        cov[2,2]=data['dcolor'][i]**2.
        cov[0,1]=data['cov_m_s'][i]
        cov[1,0] = cov[0,1]
        cov[0,2]=data['cov_m_c'][i]
        cov[2,0] = cov[0,2]
        cov[1,2]=data['cov_s_c'][i]
        cov[2,1] = cov[1,2]
        C[i*3:i*3+3,i*3:i*3+3]=cov

    return C

# similarly for sigma_diag
def diagonal_errs(zcmb):
    sigma_lens = 0.055 * zcmb
    sigma_pecvel = 5*150/3e5/(np.log(10) *zcmb)
    sigma_coh = 0.1*np.ones_like(zcmb)
    return np.column_stack((sigma_coh, sigma_lens, sigma_pecvel))

# goes into calculating covariance matrix also: dont worry about this too much
def A_fn(alpha,beta, n):
    A = np.zeros((n,3*n))
    for i in range(n):
        A[i,3*i] += 1
        A[i,3*i+1] += alpha
        A[i,3*i+2] += -beta
    return A

# yes there are globals in here (zhel, ...) which should be passed as arguments
# to this function and are not. yes, this is bad.
def run_MCMC(chains, startValues, nsteps):
    """
    this is approximately set up so that your MCMC can pick up
    where you left off. if you need to nuke everything and start again,
    remove/rename your chains directory
    """
    if os.path.isfile(chains + '/summary.txt'):
        print 'summary already exist; not running emcee again'
        return
    elif (os.path.isfile(chains + '/params.txt')) and (len(open(chains + '/params.txt').readlines())>1):
        print 'continuing from existing chains'
        pdata = np.genfromtxt(chains+'/params.txt', delimiter = ',')
        pos = pdata[-nwalkers:]
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(zhel, zcmb, mb, x1, color, thirdvar, Ceta, sigma_diag, options.model), threads=6)
        nsteps -= np.int(len(pdata)/nwalkers)
    else:
        print 'starting MCMC afresh'
        with open(chains + '/params.txt', 'w') as f3:
            f3.write('#starting MCMC on %s with %s walkers and %s steps\n'%(today_str[1:], nwalkers, nsteps))
        pos = [startValues * (1 + 0.3*np.random.randn(ndim)) for i in range(nwalkers)]
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(zhel, zcmb, mb, x1, color, thirdvar, Ceta, sigma_diag, options.model), threads=6)
    sampler.run_mcmc(pos, nsteps, storechain=False)
    print 'completed MCMC sampling'
    return

def write_summary(chains, summary, param_names, filename = 'summary.txt'):
    with open(chains + '/' + filename, 'w') as f4:
        f4.write('# chains completed; summary:\n')
        for p in param_names:
            try:
                mean = summary[p][1]
                up_err = summary[p][2] - summary[p][1]
                low_err = summary[p][1] - summary[p][0]
                f4.write('%s: %s +%s -%s\n'%(p, mean, up_err, low_err))
            except TypeError:
                pass
    print 'wrote summary of params %s to %s/summary.txt'%(param_names, chains)


if __name__ == "__main__":

    parser = OptionParser()

    ## model options: LCDM, wCDM, wCDMprior
    parser.add_option("-m", "--model", dest="model", default='LCDM',
                      help='cosmology model used for fit')

    ## specify these! these number are quite small and just for testing
    parser.add_option('-w', '--nwalkers', dest='nwalkers', default=20,
                      help='number of walkers')

    parser.add_option('-s', '--nsteps', dest='nsteps', default=50,
                      help='number of walkers')

    parser.add_option('-b', '--burnin', dest='burnin', default=0,
                      help='number of points to discard (burn in)')

    (options, args) = parser.parse_args()

    # load data
    data = #TODO
    mb = data['mb']
    x1 = data['x1']
    color = data['color']
    thirdvar = data['3rdvar']
    zcmb = data['zcmb']
    zhel = data['zhel']

    # load covariance matrix and diagonal errors using predefined functions
    Ceta = covmat_tridiagonal(data)
    sigma_diag = diagonal_errs(zcmb)

    today = datetime.date.today()
    today_str = '-%4d%02d%02d'%(today.year,today.month,today.day)

    chains = 'Chains-%s-%s'%(options.model,today_str)

    if not os.path.isdir(chains):
        os.mkdir(chains)

    nsteps = int(options.nsteps)
    nwalkers = int(options.nwalkers)
    burnin = int(options.burnin)

    if options.model.startswith('wCDM'):
        startValues = [0.3, -1, 0.15, 3, -19, -0.08]
        param_names = [r'$\Omega_m$', r'$w$', r'${\alpha}$', r'$\beta$', r'$M_B$', r'$\Delta_M$']
    else:
        startValues = [0.3, 0.15, 3, -19, -0.08]
        param_names = [r'$\Omega_m$', r'${\alpha}$', r'$\beta$', r'$M_B$', r'$\Delta_M$']
    ndim = len(startValues)

    # fitting happens here
    run_MCMC(chains, startValues, nsteps)

    pdata = np.genfromtxt(chains + '/params.txt', delimiter = ',')
    post = -0.5*np.genfromtxt(chains + '/chisq.txt', delimiter=',')
    pdata = pdata[burnin:]
    post = post[burnin:]

    # plotting and summary happens here - comment out any of the below
    c = ChainConsumer()
    c.add_chain(pdata, parameters = param_names, posterior=post)
    c.configure(statistics="max_symmetric", rainbow=True)
    summary = c.analysis.get_summary()

    # write parameter values
    write_summary(chains, summary, param_names)

    # plot contours
    fig = c.plotter.plot(figsize=(6,6), filename=chains + '/marginals-%sdim.png'%(nparams))#, blind = ['$\Omega_m$', '$w$'])
    fig.show()
    # plot walks
    fig2 = c.plotter.plot_walks(figsize=(6,6), filename=chains + '/walks-%s.png'%burnin)
    fig2.show()
