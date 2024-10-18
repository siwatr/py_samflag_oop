#!/usr/bin/env python3

from typing import Union
# Define class SamtoolsFlag to handle samtools flag values
class SamtoolsFlag:
    # Declare a class variables:
    flag_list= [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    bit_info = {
        1: "read paired",
        2: "read mapped in proper pair",
        4: "read unmapped",
        8: "mate unmapped",
        16: "read reverse strand",
        32: "mate reverse strand",
        64: "first in pair",
        128: "second in pair",
        256: "not primary alignment",
        512: "read fails platform/vendor quality checks",
        1024: "read is PCR or optical duplicate",
        2048: "supplementary alignment",
    }
    def __init__(self, bits: Union[int, list]=[False]*12):
        # NB: Bit is the only representation of the flag in this class
        # the flag property is just a getter for the bits
        self.bits = bits
    def __repr__(self):
        return f"{self.flag}"
    def __str__(self):
        # turn true/false to 1/0
        return f"SAM flag: {self.flag}:\t{[int(bit) for bit in self.bits]}"
    # Define setter and getter
    @property
    def bits(self):
        return self._bits
    @bits.setter
    def bits(self, bits):
        # check validity:
        # Bit must be a list of 12 boolean values
        if isinstance(bits, int):
            bits, r = self.flag_to_bits(bits)
            if r != 0:
                raise ValueError(f"SamtoolsFlag: Invalid flag value: {bits}, remain residual: {r}")
        if not isinstance(bits, list):
            raise ValueError("SamtoolksFlag: 'bits' attribute must be a list")
        if len(bits) != 12:
            raise ValueError("SamtoolksFlag: 'bits' must have 12 elements")
        if not all(isinstance(bit, bool) for bit in bits):
            raise ValueError("SamtoolksFlag: all element of 'bits' must be boolean")
        self._bits = bits
    # Getter and setter for flag - another way to get bits
    @property
    def flag(self):
        return self.bits_to_flag(self.bits)
    @flag.setter
    def flag(self, flag):
        # This make flag essentially the same as bits
        self.bits = flag
    # Define a method to convert flag to bits
    @staticmethod
    def flag_to_bits(flag: int) -> tuple:
        # NB: Static method don't have access to instance and class variables
        # Reverse the order of flag list
        rev_flag_list=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        rev_flag_list.reverse()
        bits = [False] * 12 # Set list corresponding to empty bits
        for i, f in enumerate(rev_flag_list):
            if flag >= f:
                bits[i] = True
                flag -= f
        bits.reverse()
        return bits, flag  # return the bits and the resudual flag for validity check
    # Define a method to convert bits to flag
    @staticmethod
    def bits_to_flag(bits: list) -> int:
        flag = 0
        for i, b in enumerate(bits):
            if b:
                flag += 2**i
        return flag


def main():
    f = SamtoolsFlag(4)
    f
    print(f)
    # Test setter
    f.bits = 1
    print(f)
    f.bits = [True]*12
    print(f)
    print(f.flag)
    print(f.bits)
    f.flag = 12
    print(f)
    try: 
        print(SamtoolsFlag(5000))
    except ValueError:
        print("Declare got value error as expected")
    try: 
        f.bits = 5000
    except ValueError:
        print("set f.bits got value error as expected")
    try: 
        f.flag = 5000
    except ValueError:
        print("set f.flag got value error as expected")


if __name__ == '__main__':
    main()
