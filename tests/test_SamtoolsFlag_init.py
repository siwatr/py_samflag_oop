#!/usr/bin/env python3

import sys
import os
import pytest

# Re root: to allow import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(os.getcwd())

# from src.SamtoolsFlag.SamtoolsFlag import SamtoolsFlag
from SamtoolsFlag.SamtoolsFlag import SamtoolsFlag

def test_init_int():
    assert SamtoolsFlag().bits == [False]*12
    assert SamtoolsFlag(0).bits == [False]*12
    assert SamtoolsFlag(4095).bits == [True]*12

def test_init_boolList():
    assert SamtoolsFlag([True] * 12).bits == [True] * 12
    assert SamtoolsFlag([False] * 12).bits == [False] * 12
    for i in range(1, 13):
        b = [True] * i
        if i == 12:
            assert SamtoolsFlag(b).bits == b
        else:
            with pytest.raises(ValueError):
                SamtoolsFlag(b)

def test_init_int_vs_list():
    b = [False]*12
    for i in range(12):
        b[i] = True
        b1 = SamtoolsFlag(2**i).bits
        b2 = SamtoolsFlag(b.copy()).bits
        b[i] = False
        assert b1 == b2

def test_individual_bit():
    # DEPRECIATED: explicatly define and test each bit -> Switch to use the loop version
    # assert SamtoolsFlag(1).bits    == [True, False, False, False, False, False, False, False, False, False, False, False]
    # assert SamtoolsFlag(2).bits    == [False, True, False, False, False, False, False, False, False, False, False, False]
    # assert SamtoolsFlag(4).bits    == [False, False, True, False, False, False, False, False, False, False, False, False]
    # assert SamtoolsFlag(8).bits    == [False, False, False, True, False, False, False, False, False, False, False, False]
    # assert SamtoolsFlag(16).bits   == [False, False, False, False, True, False, False, False, False, False, False, False]
    # assert SamtoolsFlag(32).bits   == [False, False, False, False, False, True, False, False, False, False, False, False]
    # assert SamtoolsFlag(64).bits   == [False, False, False, False, False, False, True, False, False, False, False, False]
    # assert SamtoolsFlag(128).bits  == [False, False, False, False, False, False, False, True, False, False, False, False]
    # assert SamtoolsFlag(256).bits  == [False, False, False, False, False, False, False, False, True, False, False, False]
    # assert SamtoolsFlag(512).bits  == [False, False, False, False, False, False, False, False, False, True, False, False]
    # assert SamtoolsFlag(1024).bits == [False, False, False, False, False, False, False, False, False, False, True, False]
    # assert SamtoolsFlag(2048).bits == [False, False, False, False, False, False, False, False, False, False, False, True]
    b = [False]*12
    B = []
    for i in range(len(b)):
        b[i] = True
        # B.append(b)
        B.append(b.copy()) # appending the bytearray copy, not the reference
        b[i] = False
    print(*B, sep="\n")
    # Test
    for i in range(len(B)):
        assert SamtoolsFlag(2**i).bits == B[i]

# Test all possible values:
def test_all_values_init():
    for i in range(4096):
        assert SamtoolsFlag(i).bits

def test_neg_init():
    with pytest.raises(ValueError):
        SamtoolsFlag(-1)
    with pytest.raises(ValueError):
        SamtoolsFlag(-20)

def test_big_value():
    # Maximum value is 4095
    with pytest.raises(ValueError):
        SamtoolsFlag(4096)
    with pytest.raises(ValueError):
        SamtoolsFlag(5000)

def test_type():
    with pytest.raises(ValueError):
        SamtoolsFlag("one")
    with pytest.raises(ValueError):
        SamtoolsFlag("T"*12) # String with lenght of 12
    with pytest.raises(ValueError):
        SamtoolsFlag("0" * 12)  # String with lenght of 12
    with pytest.raises(ValueError):
        SamtoolsFlag("1")
    with pytest.raises(ValueError):
        SamtoolsFlag([1])
    with pytest.raises(ValueError):
        SamtoolsFlag(1.0)
    with pytest.raises(ValueError):
        SamtoolsFlag(True)

# To test, run pytest ./test/test_SamtoolsFlag_init.py
