"""
Represents one disassembled 6502 instruction.
"""

from dataclasses import dataclass


@dataclass
class Instruction:
    """One decoded instruction."""

    address: int
    bytes: list[int]
    mnemonic: str
    operand: str

    def __str__(self):

        byte_string = " ".join(
            f"{byte:02X}" for byte in self.bytes
        )

        return (
            f"{self.address:04X}  "
            f"{byte_string:<8} "
            f"{self.mnemonic:<3} "
            f"{self.operand}"
        )