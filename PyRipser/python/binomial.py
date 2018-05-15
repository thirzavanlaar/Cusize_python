#!/usr/bin/env python

import numpy as np
import scipy.special as sc

class BinomialCoeffTable(object):
    """
    n : int
    k : int
    """
    def __init__(self, n, k):
        self.n_max = n
        self.k_max = k
        self.B = sc.binom.outer(
            np.array(range(n+1), dtype=np.int64), 
            np.array(range(k+1), dtype=np.int64))

    def __call__(self, n, k):
        assert(n <= self.n_max)
        assert(k <= self.k_max)
        return int(self.B[n][k])


if __name__ == '__main__':
    table = BinomialCoeffTable(100, 10)
    print table.B.shape


