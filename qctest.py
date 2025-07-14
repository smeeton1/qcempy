#unit test for qcempy

import qcempy as qc
import numpy as np
import pytest

def test_MPS():
    MPStest = qc.MPS(3)
    assert len(MPStest.qbit) ==3
    assert len(MPStest.Lambda) ==3
    assert len(MPStest.order) ==3
    assert (MPStest.qbit[0] == [0,1]).all()
    assert (MPStest.qbit[1] == [0,1]).all()
    assert (MPStest.qbit[2] == [0,1]).all()
    assert (MPStest.Lambda[0] == [1]).all()
    assert (MPStest.Lambda[1] == [1]).all()
    assert (MPStest.Lambda[2] == [1]).all()
    assert (MPStest.order[0] == [0]).all()
    assert (MPStest.order[1] == [1]).all()
    assert (MPStest.order[2] == [2]).all()
    assert MPStest.error == 0.01