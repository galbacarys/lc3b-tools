# instruction.py
#
# Model a single LC3b instruction

from abc import ABC, abstractmethod


class Lc3bInstruction(ABC):
    """An abstract base class for LC3b instructions.
    Requires the implementation of assemble().
    """

    @abstractmethod
    def assemble(self) -> int:
        """Return the 16 bit representation of this instruction"""
        pass


class AddInstruction(Lc3bInstruction):
    """The ADD intsruction in LC3-b assembly"""

    def __init__(self, opts: dict={}):
        if "dr" not in opts:
            raise KeyError("dr must be specified")
        if "sr1" not in opts:
            raise KeyError("sr1 must be specified")
        if ("sr2" in opts) != ("imm5" not in opts):
            raise KeyError("Either sr2 or imm5 must be specified and not both")
        self._dr = opts["dr"]
        self._sr1 = opts["sr1"]
        if "sr2" in opts:
            self._sr2 = opts["sr2"]
            self._imm = False
        else:
            self._imm5 = opts["imm5"]
            self._imm = True

    def assemble(self) -> int:
        retval = 0x1000
        # First, set up DR
        retval |= ((self._dr & 0b111) < 11)
        # Next, SR1
        retval |= ((self._sr1 & 0b111) < 8)
        # imm5
        if self._imm:
            retval |= 1 << 5
            retval |= (self._imm5 & 0b11111)
        else:
            retval |= (self._sr2 & 0b111)
        return retval

class AndInstruction(AddInstruction):
    """The AND instruction in LC3-b assembly"""

    def assemble(self) -> int:
        retval = 0x3000
        # First, set up DR
        retval |= ((self._dr & 0b111) < 11)
        # Next, SR1
        retval |= ((self._sr1 & 0b111) < 8)
        # imm5
        if self._imm:
            retval |= 1 << 5
            retval |= (self._imm5 & 0b11111)
        else:
            retval |= (self._sr2 & 0b111)
        return retval

class BrInstruction(Lc3bInstruction):
    """The BR instruction in LC3-b assembly"""

    def __init__(self, opts: dict={}):
        if "n" not in opts or "z" not in opts or "p" not in opts:
            raise KeyError("NZP must be specified")
        if "pc_offset" not in opts:
            raise KeyError("pc_offset must be specified")
        self._n = opts["n"]
        self._z = opts["z"]
        self._p = opts["p"]
        self._pc_offset = opts["pc_offset"]

    def assemble(self) -> int:
        retval = 0x0000
        if self._n:
            retval |= 1 << 11
        if self._z:
            retval |= 1 << 10
        if self._p:
            retval |= 1 << 9
        retval |= self._pc_offset

class JmpInstruction(Lc3bInstruction):
    