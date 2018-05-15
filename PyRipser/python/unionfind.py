#!/usr/bin/env python
import numpy as np
class UnionFind(object):

    def __init__(self, n):
        """
        n : int
        """
        self.parent = np.array(range(n), dtype=np.int64)
        self.rank = np.zeros(n, dtype=np.uint8)

    def find(self, x):
        """
        x : int
        return z : int
        """
        y = x
        z = self.parent[x]
        while z != y:
            y = z
            z = self.parent[y]
        y = self.parent[x]
        while z != y:
            self.parent[x] = z
            x = y
            y = self.parent[x]
        return z

    def link(self, x, y):
        """
        x : int
        y : int
        return : void
        """
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.rank[x] > self.rank[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1

if __name__ == '__main__':
    uf = UnionFind(16)
    uf.link(12, 13);
    uf.link(14, 13);
    uf.link(0, 3);
    uf.link(1, 3);
    uf.link(2, 3);
    uf.link(7, 3);
    uf.link(12, 7);
    uf.link(10, 14);
    uf.link(11, 14);
    uf.link(8, 10);
    uf.link(9, 10);
    uf.link(15, 8);
    uf.link(6, 9);
    uf.link(4, 15);
    uf.link(5, 15);

    p = np.array([ 3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3, 13,  3,  3,  3])
    assert(all(uf.parent == p))
    r = np.array([0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    assert(all(uf.rank == r))