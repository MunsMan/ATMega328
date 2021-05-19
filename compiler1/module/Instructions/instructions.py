from . import twoOp
from typing import Callable
from ..errorHandling.error import throwError


def mapInstructions(opcode: str) -> Callable:
    if opcode in InstructionsMap:
        return InstructionsMap[opcode]
    throwError(4, True, (opcode))


def ldi(rd: int, k: int) -> int:
    opcode = 0xE000
    kh = (k & 0xF0) << 4
    kl = k & 0xF
    dest = (rd - 16) << 4
    return opcode + kh + dest + kl

def mov(rd: int, rr: int) -> int:
    return (0b001011 << 10) + twoOp(rd, rr)


def add(rd: int, rn: int) -> int:
    return (3 << 10) + twoOp(rd, rn)


def logicalAndIm(rd: int, k: int) -> int:
    opcode = 0x7 << 12
    kh = (k & 0xF0) << 4
    kl = (k & 0xF)
    d = rd << 4
    return opcode + kh + d + kl


def shiftRight(rd: int) -> int:
    opcode = 0x9405
    d = rd << 4
    return opcode + d


def clearBitSREG(rd: int) -> int:
    opcode = 0x9488
    s = rd << 4
    return opcode + s


def loadBitT(rd: int, rr: str) -> int:
    opcode = 0xF800
    rd = rd << 4
    return opcode + rd + rr


def brbc(rd: int, rr: int):
    opcode = 0xF400
    k = rr << 3
    return opcode + k + rd


InstructionsMap = {
    "ldi": ldi,
    "mov": mov,
    "add": add,
    "brbc": brbc,
}
