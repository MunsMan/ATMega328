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


def adc(rd: int, rn: int) -> int:
    return (7 << 10) + twoOp(rd, rn)


def andi(rd: int, immediate: int) -> int:
    opcode = 0x7 << 12
    kh = (immediate & 0xF0) << 4
    kl = (immediate & 0xF)
    d = rd << 4
    return opcode + kh + d + kl


def and_(rd: int, rr: int) -> int:
    opcode = 0x08 << 10
    r = ((rr & 0x10) << 5) + (rr & 0x0F)
    d = ((rd & 0x10) << 3) + ((rd & 0x0F) << 4)
    return opcode + r + d


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
    s = rd
    k = rr << 3
    return opcode + k + s


def brbs(rd: int, rr: int) -> int:
    opcode = 0xF << 12
    s = rd
    k = rr << 3
    return opcode + k + s


InstructionsMap = {
    "ldi": ldi,
    "mov": mov,
    "add": add,
    "brbc": brbc,
    "brbs": brbs,
    "and": and_,
    "andi": andi
}
