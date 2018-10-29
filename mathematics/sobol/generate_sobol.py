""" Module to compute Sobol sequences as adapted from SALib:
    >> github.com/SALib/SALib
#==============================================================================
# The following code is based on the Sobol sequence generator by Frances
# Y. Kuo and Stephen Joe. The license terms are provided below.
#
# Copyright (c) 2008, Frances Y. Kuo and Stephen Joe
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the names of the copyright holders nor the names of the
# University of New South Wales and the University of Waikato
# and its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#==============================================================================
"""

import sys

import numpy as np
from directions import directions

if sys.version_info[0] > 2:
    long = int

n_samples = 1000
lowest_startingpoint = 100
highest_startingpoint = 2000


def sample(N, D, start=1):
    """Generate (N x D) numpy array of Sobol sequence samples"""
    scale = 31
    result = np.zeros([N, D])

    if D > len(directions) + 1:
        raise ValueError("Error in Sobol sequence: not enough dimensions")

    L = int(np.ceil(np.log(N) / np.log(2)))

    if L > scale:
        raise ValueError("Error in Sobol sequence: not enough bits")

    for i in range(D):
        V = np.zeros(L + 1, dtype=np.int64)

        if i == 0:
            for j in range(1, L + 1):
                V[j] = 1 << (scale - j)  # all m's = 1
        else:
            m = np.array(directions[i - 1], dtype=int)
            a = m[0]
            s = len(m) - 1

            # The following code discards the first row of the ``m`` array
            # Because it has floating point errors, e.g. values of 2.24e-314
            if L <= s:
                for j in range(1, L + 1):
                    V[j] = m[j] << (scale - j)
            else:
                for j in range(1, s + 1):
                    V[j] = m[j] << (scale - j)
                for j in range(s + 1, L + 1):
                    V[j] = V[j - s] ^ (V[j - s] >> s)
                    for k in range(1, s):
                        V[j] ^= ((a >> (s - 1 - k)) & 1) * V[j - k]

        X = long(0)
        for j in range(start, N + start - 1):
            X ^= V[index_of_least_significant_zero_bit(j - 1)]
            result[j][i] = float(X / np.power(2, scale))

    return result


def index_of_least_significant_zero_bit(value):
    index = 1
    while (value & 1) != 0:
        value >>= 1
        index += 1

    return index

def rand(dimension, nmax=n_samples, low=lowest_startingpoint, 
         high=highest_startingpoint, seed=None):
    """ Return quasi random number similar to np.random.rand
    
    Arguments:
        dimension {int} -- dimension of each sample
        nmax{int} -- number of samples (default: 1000)
    
    Keyword Arguments:
        low {int} -- discard this many values (default: {100})
        high {int} -- maximum number to start Sobol series (default: {2000})
        seed {int} -- seed for initializing the starting point (default: {None})
    
    Returns:
        np.ndarray -- requested list of quasi random numbers
    """

    if seed:
        rng = np.random.RandomState(seed)
    else:
        rng = np.random
    
    # Choose the starting point of the Sobol sequence. Similar to a seed.
    startpoint = rng.randint(low=low, high=high)
    sobol_sequence = sample(nmax + startpoint, dimension)

    return sobol_sequence[startpoint:, :]

class QuasiRandomState:
    """ Similar to np.random.RandomState, but for Sobol sequences """

    def __init__(self, dimension=None, nmax=n_samples, 
                 low=lowest_startingpoint, high=highest_startingpoint,
                 seed=None):
        """ Initialize the QuasiRandomState """
        
        self.nmax = nmax
        self.dimension = dimension
        self.low = low
        self.high = high
        self.seed = seed
        
        if dimension is not None:
            self.sequence = iter(rand(dimension, nmax, low, high, seed))
        else:
            self.sequence = None

    def rand(self, dimension=None):
        """ Rand method that yields Sobol sequences of dimension D """
        if self.sequence is None:
            self.sequence = iter(rand(dimension, self.nmax, self.low, 
                                      self.high, self.seed))
            self.dimension = dimension

        if dimension != self.dimension:
            raise Exception('Dimension changed.')

        return next(self.sequence)