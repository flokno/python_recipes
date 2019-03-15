# Statistics module
import numpy as np
from   scipy import linalg as la

def test():
    print('test')

# Correlation functions
def correlate(s1, s2, mode='full'):
    # check shape
    if s1.shape != s2.shape:
        print(f'Correlate: Shape of signal1= {s1.shape} != shape of signal2= {s2.shape}')
        exit('  Not yet implemented. Break.')
    #
    if mode=='full':
        return correlate_full(s1, s2)
    if mode=='same':
        return correlate_same(s1, s2)

def correlate_full(s1, s2):
    N = len(s1)
    Ncorr = 2*N - 1
    corr = np.zeros((Ncorr, *tuple(s1.shape[1:])))
    # pad with zeros
    c1 = np.zeros((Ncorr, *tuple(s1.shape[1:])))
    c1[N-1:] = s1
    c2 = np.zeros((Ncorr, *tuple(s1.shape[1:])))
    c2[:N] = s2

    corr = np.zeros((Ncorr, *tuple(s1.shape[1:])))

    for ii in range(Ncorr):
        roll = np.roll(c2, ii, axis=0)
        #print(roll)
        corrtemp = (c1 * roll).sum(axis=0)
        #print(corrtemp)
        corr[ii] =  corrtemp
    #
    return corr

def correlate_same(s1, s2):
    fc = correlate_full(s1, s2)
    Ncorr = len(fc)
    N = (Ncorr + 1) //2
    # pick middle part
    return(fc[ (N-1)//2 : Ncorr - N//2])

# Fourier Transforms
def fft(signal):
    N = len(signal)
    Ft = np.zeros(signal.shape, dtype=complex)
    ns = np.arange(N)
    im = np.complex(0, 1)
    for kk in range(N):
        Ft[kk] = np.exp(-2*np.pi*im * kk * ns / N) @ signal
    return Ft

def ifft(signal):
    N = len(signal)
    iFt = np.zeros(signal.shape, dtype=complex)
    ks = np.arange(N)
    im = np.complex(0, 1)
    for nn in range(N):
        iFt[nn] = np.exp(2*np.pi*im * ks * nn / N) @ signal
    return iFt / N

