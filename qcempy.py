# a small quantum circuit emulator wirten in python using numpy
# does not intergrate noise and only have the mps method.

import numpy as np


class MPS:
    # Class to hold the MPS data 
    # setup n q-tensor and n-1 l-tensor
    # set up order 0 - n array
    # set error for svd
     def __init__(self, N = 1, error = 0.01):
            self.qbit = [np.array([0,1]) for _ in range(N)]
            self.Lambda = [np.array([1]) for _ in range(N)]
            self.order = np.array(range(0,N))
            self.error = error