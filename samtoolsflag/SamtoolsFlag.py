#!/usr/bin/env python3


from typing import Union
import copy
# Define a class SamtoolsBits to handle the bit part of the SamtoolsFlag
class SamtoolsBits:
    # A subclass of SamtoolsFlag
    # On the surface SamtoolsBits should behave like a list
    def __init__(self, bits):
        self.bits = bits
    @staticmethod
    def validate_bits(bits):
        valid=False
        if not isinstance(bits, list):
            raise ValueError("'bits' must be a list type")
        if len(bits) != 12:
            raise ValueError("'bits' must have 12 elements")
        if not all(isinstance(item, bool) for item in bits):
            raise ValueError("'bits' must be a list of 12 boolean values")
        else:
            # print("Valid bits") # for debugging
            valid=True
        return valid
    def validate(self):
        valid = self.validate_bits(self.bits)
        return valid
    @property
    def bits(self):
        return self._bits
    @bits.setter
    def bits(self, bits):
        if(isinstance(bits, SamtoolsBits)):
            bits = bits._bits.copy() # Use copy function to avoid reference
        if self.validate_bits(bits):
            self._bits = bits
    # Subsetting methods
    def __getitem__(self, index):
        return self.bits[index]
    def __setitem__(self, index, value):
        # print("Set bit from index") # For debugging
        bits = self._bits.copy()
        bits[index] = value
        if self.validate_bits(bits):
            self._bits = bits
    def __len__(self):
        return len(self.bits)
    def __repr__(self):
        return repr(self.bits)
    def __eq__(self, other) -> bool:
        if isinstance(other, SamtoolsBits):
            return self._bits == other._bits
        else:
            return self._bits == other
    # When we want to copy the object
    def __copy__(self):
        return SamtoolsBits(copy.deepcopy(self._bits))
    def copy(self):
        return self.__copy__()


# Define class SamtoolsFlag to handle samtools flag values
class SamtoolsFlag:
    # Declare a class variables:
    flag_list= [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    bit_info = [
        "read paired",
        "read mapped in proper pair",
        "read unmapped",
        "mate unmapped",
        "read reverse strand",
        "mate reverse strand",
        "first in pair",
        "second in pair",
        "not primary alignment",
        "read fails platform/vendor quality checks",
        "read is PCR or optical duplicate",
        "supplementary alignment",
    ]
    # build a dictionary from flag_list (keys) and bit_info (values)
    bit_info_dict = dict(zip(flag_list, bit_info))
    def __init__(self, bits: Union[int, list]=[False]*12):
        # Representing Samtools flag as a list of 12 boolean values -> represented by SamtoolsBits class
        # Other attributes, such as flag and bit_comb can be derived from this list
        self.bits = bits
    def __repr__(self):
        return f"SAM Flag: {self.flag}"
    def __str__(self):
        # turn true/false to 1/0
        return f"SAM flag: {self.flag}:\t{[int(bit) for bit in self.bits]}"
    # Define setter and getter
    @property
    def bits(self):
        return self._bits # should now be a SamtoolsBits object
    @bits.setter
    def bits(self, bits: Union[int, list, SamtoolsBits]):
        # Transform alternative input types to list, then feed to SamtoolsBits()
        b=bits # Backup value for raise error
        if isinstance(bits, bool):
            # NB: True, False can be interpreted as int, so we have to check this first
            raise ValueError(f"A single boolean value: {bits} is invalid")
        if isinstance(bits, int):
            if bits < 0:
                raise ValueError(f"SamtoolsFlag: Flag value must be a zero or positive value. Given flag: {b}")
            bits, r = self.flag_to_bits(bits)
            if r != 0:
                raise ValueError(f"SamtoolsFlag: Invalid flag value: {b}.\n\tThe value cannot be fit to 12 bits information.\n\tRemain residual: {r}")
        # Set values
        if isinstance(bits, list):
            # DEPRECIATED: Validate give the list validation to SamtoolsBits class instead
            # if len(bits) != 12:
            #     raise ValueError("SamtoolksFlag: 'bits' must have 12 elements")
            # if not all(isinstance(bit, bool) for bit in bits):
            #     raise ValueError("SamtoolksFlag: all element of 'bits' must be boolean")
            self._bits = SamtoolsBits(bits)
        elif isinstance(bits, SamtoolsBits):
            bits.validate() # just to be sure
            self._bits = bits
        else:
            raise ValueError("SamtoolksFlag: Please use variable from one of these classes to set the 'bits' attribute: int, list (12 boolean elements), and SamtoolsBits")
    # No need to set __getitem__ and __setitem__ for bits as this will be handled by SamtoolsBits class
    # Getter and setter for flag - another way to get bits
    @property
    def flag(self):
        return self.bits_to_flag(self.bits)
    @flag.setter
    def flag(self, flag: int):
        # This make flag essentially the same as bits
        self.bits = flag
    # Getter of individual bit number
    @property 
    def bit_comb(self):
        return [2**i for i, bit in enumerate(self.bits) if bit]
    @bit_comb.setter
    def bit_comb(self, bit_comb: list):
        if not isinstance(bit_comb, list):
            raise ValueError("SamtoolsFlag: 'bit_comb' must be a list")
        if not all(isinstance(bit, int) for bit in bit_comb):
            raise ValueError("SamtoolsFlag: all element of 'bit_comb' must be integer")
        # Check for redundancy
        if len(bit_comb) != len(set(bit_comb)):
            raise ValueError("SamtoolsFlag: 'bit_comb' must not have redundant values")
        if len(bit_comb) > 12:
            raise ValueError("SamtoolsFlag: 'bit_comb' can only have up to 12 elements")
        if any(bit not in self.flag_list for bit in bit_comb):
            raise ValueError("SamtoolsFlag: Invalid bit combination")
        # Set through flag setter
        self.flag = sum(bit_comb)
    # Define a method to convert flag to bits
    @staticmethod
    def flag_to_bits(flag: int) -> tuple:
        # NB: Static method don't have access to instance and class variables
        rev_flag_list=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        rev_flag_list.reverse()  # Reverse the order of flag list
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
    def explain(self):
        """Explain what's the current SAM flag means"""
        # if not isinstance(self, "SamtoolsFlag"):
        #     raise ValueError("SamtoolsFlag: Invalid operand")
        for i, bit in enumerate(self.bits):
            if bit:
                print(f"Bit {self.flag_list[i]}:\t{self.bit_info[i]}")
    # Operation Overload
    def __add__(self, other: Union[int, "SamtoolsFlag"]) -> "SamtoolsFlag":
        if isinstance(other, int) or isinstance(other, list):
            other = SamtoolsFlag(other)
        elif not isinstance(other, SamtoolsFlag):
            raise ValueError("SamtoolsFlag: Invalid operand")
        bits = [a or b for a, b in zip(self.bits, other.bits)]
        return SamtoolsFlag(bits)
    # overload += operator
    def __iadd__(self, other: Union[int, "SamtoolsFlag"]) -> "SamtoolsFlag":
        self = self + other
        return self
    # Overload the - operator
    # Not sure if this is biologically meaningful
    def __sub__(self, other: Union["SamtoolsFlag", int, list]) -> "SamtoolsFlag":
        if isinstance(other, int) or isinstance(other, list):
            other = SamtoolsFlag(other)
        elif not isinstance(other, SamtoolsFlag):
            raise ValueError("SamtoolsFlag: Invalid operand")
        bits = [a and not b for a, b in zip(self.bits, other.bits)]
        return SamtoolsFlag(bits)
    # overload 'in' operation
    def __contains__(self, other: Union["SamtoolsFlag", int, list]) -> bool:
        if isinstance(other, int) or isinstance(other, list):
            other = SamtoolsFlag(other)
        elif not isinstance(other, SamtoolsFlag):
            raise ValueError("SamtoolsFlag: Invalid operand")
        # For bit pair that is True in A, are they all True in B?
        ans = all([b for a, b in zip(self.bits, other.bits) if a])
        # alternative method
        ans = (self + other).flag == self.flag
        return ans
    def __eq__(self, other: Union["SamtoolsFlag", int, list]) -> bool:
        if isinstance(other, int) or isinstance(other, list):
            other = SamtoolsFlag(other)
        elif not isinstance(other, SamtoolsFlag):
            raise ValueError("SamtoolsFlag: Invalid operand")
        return self.flag == other.flag
    def __copy__(self):
        return SamtoolsFlag(copy.deepcopy(self._bits))
    def copy(self):
        return self.__copy__()

