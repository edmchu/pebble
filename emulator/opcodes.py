"""
6502 Opcode Definitions
"""

from enum import Enum


class AddressingMode(Enum):

    IMPLIED = 0

    ACCUMULATOR = 1

    IMMEDIATE = 2

    ZERO_PAGE = 3
    ZERO_PAGE_X = 4
    ZERO_PAGE_Y = 5

    ABSOLUTE = 6
    ABSOLUTE_X = 7
    ABSOLUTE_Y = 8

    INDIRECT = 9

    INDEXED_INDIRECT = 10
    INDIRECT_INDEXED = 11

    RELATIVE = 12