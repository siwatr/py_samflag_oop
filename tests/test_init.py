#!/usr/bin/env python3

import sys
import os
import pytest

# Re root: to allow import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(os.getcwd())

# from src.SamtoolsFlag.SamtoolsFlag import SamtoolsFlag
from SamtoolsFlag.SamtoolsFlag import SamtoolsFlag

print(SamtoolsFlag(1))
