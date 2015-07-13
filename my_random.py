import numpy as np
from pattern import DF_Pattern


class MyRandom(DF_Pattern):
    def __init__(self, *args, **kargs):
        DF_Pattern.__init__(self, *args, **kargs)

    def step(self):
        for _ in xrange(self.rows*self.cols*3):
            data = np.rand() * 255
            data