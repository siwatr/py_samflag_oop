#!/usr/bin/env python3

import sys
import os
import pytest

# Re root: to allow import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(os.getcwd())

# from src.SamtoolsFlag.SamtoolsFlag import SamtoolsFlag
from SamtoolsFlag.SamtoolsFlag import SamtoolsFlag
from SamtoolsFlag.SamtoolsFlag import SamtoolsBits
# import SamtoolsFlag.SamtoolsFlag

def test_class():
    assert isinstance(SamtoolsFlag(1), SamtoolsFlag)
    assert isinstance(SamtoolsFlag(1).bits, SamtoolsBits)
    assert isinstance(SamtoolsFlag(1)._bits, SamtoolsBits)
    assert isinstance(SamtoolsFlag(1)._bits._bits, list)
    assert all([isinstance(b, bool) for b in SamtoolsFlag(1).bits])
    assert isinstance(SamtoolsFlag(1).flag, int)
    assert isinstance(SamtoolsFlag(0).bit_comb, list)
    assert isinstance(SamtoolsFlag(1).bit_comb, list)
    assert isinstance(SamtoolsFlag(4095).bit_comb, list)

def test_bits():
    assert SamtoolsFlag(0).bits == [False] * 12

def test_flag():
    """Test that it's return the same value as the value used for initilization"""
    for i in range(4096):
        assert SamtoolsFlag(i) == i

def test_bit_comb():
    assert len(SamtoolsFlag(0).bit_comb) == 0
    assert len(SamtoolsFlag(1).bit_comb) == 1
    assert len(SamtoolsFlag(4095).bit_comb) == 12
