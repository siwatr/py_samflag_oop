#!/usr/bin/env python3

import sys
import os
import pytest

# Re root: to allow import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(os.getcwd())

# from src.SamtoolsFlag.SamtoolsFlag import SamtoolsFlag
from SamtoolsFlag.SamtoolsFlag import SamtoolsFlag


def test_set_bits():
    f = SamtoolsFlag()
    f.bits = [True] * 12
    assert f.flag == 4095
    f.bits[0] = False # Edit by slicing
    assert f.flag == 4094


def test_set_bits_index():
    f = SamtoolsFlag()
    f.bits[0] = True
    assert f.bits == [True] + [False] * 11
    f.bits[1] = True
    assert f.bits == [True, True] + [False] * 10


def test_copy():
    f1 = SamtoolsFlag(16)
    f2 = f1.copy()
    assert f1.flag == f2.flag
    assert isinstance(f2, SamtoolsFlag) # Still the same class
    assert f1 is not f2
    f2.bits[0] = True
    assert f1.flag != f2.flag


def test_set_bits_index_err():
    f = SamtoolsFlag()
    # Wrong setting
    with pytest.raises(ValueError):
        f.bits[0] = "True"
    with pytest.raises(ValueError):
        f.bits[0] = 1
    with pytest.raises(ValueError):
        f.bits[0] = 2
    with pytest.raises(ValueError):
        f.bits[0] = [True]

