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
from warnings import warn

import numpy as np
from directions import directions

if sys.version_info[0] > 2:
    long = int

n_samples = 5000
lowest_startingpoint = 100
highest_startingpoint = 500


def sample(N, D):
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
        for j in range(1, N):
            X ^= V[index_of_least_significant_zero_bit(j - 1)]
            result[j][i] = float(X / np.power(2, scale))

    return result


def index_of_least_significant_zero_bit(value):
    index = 1
    while (value & 1) != 0:
        value >>= 1
        index += 1

    return index


def rand(
    nsamples,
    dimension,
    low=lowest_startingpoint,
    high=highest_startingpoint,
    randomize=False,
    seed=None,
):
    """ Return quasi random number similar to np.random.rand

    Arguments:
        nsamples {int} -- number of samples
        dimension {int} -- dimension of each sample

    Keyword Arguments:
        low {int} -- discard this many values (default: {500})
        high {int} -- maximum number to start Sobol series (default: {1000})
        randomize {bool} -- further randomize the sample afterwards
        seed {int} -- seed for initializing the starting point (default: {None})

    Returns:
        np.ndarray -- requested list of quasi random numbers
    """

    if seed:
        rng = np.random.RandomState(seed)
    else:
        rng = np.random

    # Choose the starting point of the Sobol sequence. Similar to a seed.
    if randomize:
        startpoint = rng.randint(low=low, high=high + low)
    else:
        startpoint = low
    sobol_sequence = sample(nsamples + startpoint, dimension)[startpoint:, :]

    if randomize:
        # Randomize by adding random number mod 1
        sobol_sequence = (sobol_sequence + np.random.rand()) % 1

    return sobol_sequence


class RandomState:
    """ Similar to np.random.RandomState, but for Sobol sequences """

    def __init__(
        self,
        dimension,
        nmax=n_samples,
        low=lowest_startingpoint,
        high=highest_startingpoint,
        randomize=False,
        seed=None,
    ):
        """ Initialize the QuasiRandomState for samples of specific dimension

        Args:
            dimension (int): dimension of the samples
            nmax (int, optional): maximum number of samples (5000)
            low (int, optional): skip this many samples (100)
            high (int, optional): skip this many samples (max)
            randomize (bool, optional): further randomize the sample
            seed (int, optional): seed for further randomization
        """

        self.nmax = nmax
        self.low = low
        self.high = high
        self.randomize = randomize
        self.seed = seed
        self.dimension = np.asarray(dimension)

        # generate the sequence
        self.sequence = iter(
            rand(nmax, self.dimension.prod(), low, high, randomize, seed)
        )

    def rand(self, sample_dimension=1):
        """ return sample of specific dimension from the Sobol sequence

        Args:
            samples_dimension (int, optional): Dimension of samples to return

        Returns:
            ndarray: samples from the Sobol sequence
        """

        # Make sure the sample_dimension is  an ndarray and has .prod()
        sample_dimension = np.asarray(sample_dimension)
        n_samples = sample_dimension.prod()
        n_samples_to_draw = n_samples // self.dimension.prod() + 1

        # Warn User if the initialization is not commensurate with the sample asked for
        if n_samples % self.dimension.prod() != 0:
            print(f"Number for samples:     {n_samples}")
            print(f"Initializing dimension: {self.dimension.prod()}")
            warn(
                "Number of samples not commensurate with the initializing dimension."
                + " Do not expect to receive quasi random numbers."
            )

        sample = [next(self.sequence) for _ in range(n_samples_to_draw)]
        sample = np.array(sample)

        return np.squeeze(sample.flatten()[:n_samples].reshape(sample_dimension))
