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


def adiw(rd: int, rr: int) -> int:
    opcode = 0x9600
    destination = ((rd - 24) // 2) << 4
    immediate = ((rr & 0x30) << 2) + (rr & 0xF)
    return opcode + destination + immediate


def and_(rd: int, rr: int) -> int:
    opcode = 0x08 << 10
    r = ((rr & 0x10) << 5) + (rr & 0x0F)
    d = ((rd & 0x10) << 3) + ((rd & 0x0F) << 4)
    return opcode + r + d


def andi(rd: int, immediate: int) -> int:
    opcode = 0x7 << 12
    kh = (immediate & 0xF0) << 4
    kl = (immediate & 0xF)
    d = rd << 4
    return opcode + kh + d + kl


def asr(rd: int) -> int:
    opcode = 0x9405
    d = rd << 4
    return opcode + d


def bclr(rd: int) -> int:
    opcode = 0x9488
    s = rd << 4
    return opcode + s


def bld(rd: int, rr: str) -> int:
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


def bset(rd: int) -> int:
    opcode = 0x9408
    rd <<= 4
    return opcode + rd


def bst(rd: int, rr: int) -> int:
    opcode = 0xFA00
    rd <<= 4
    return opcode + rd + rr


def call(rd: int) -> int:
    opcode = 0x940E0000
    return opcode + rd


def cbi(rd: int, rr: int) -> int:
    opcode = 0x9800
    return opcode + (rd << 3) + rr


def clc() -> int:
    return 0x9488


def clh() -> int:
    return 0x94D8


def cli() -> int:
    return 0x94F8


def cln() -> int:
    return 0x94A8


def clr(rd: int) -> int:
    opcode = 0x2400
    return opcode + rd


def cls() -> int:
    return 0x94C8


def clt() -> int:
    return 0x94E8


def clv() -> int:
    return 0x94B8


def clz() -> int:
    return 0x9498


def com(rd: int) -> int:
    opcode = 0x9400
    return opcode + (rd << 4)


def cp(rd: int, rr: int) -> int:
    opcode = 0x1400
    return opcode + twoOp(rd, rr)


def cpc(rd: int, rr: int) -> int:
    opcode = 0x0400
    return opcode + twoOp(rd, rr)


def cpi(rd: int, rr: int) -> int:
    opcode = 0x3000
    immediate = ((rr & 0xF0) << 4) + (rr & 0x0F)
    return opcode + immediate + (rd << 4)


def cpse(rd: int, rr: int) -> int:
    opcode = 0x1000
    return opcode + twoOp(rd, rr)


def dec(rd: int) -> int:
    opcode = 0x940A
    return opcode + (rd << 4)


def des(rd: int) -> int:
    opcode = 0x940B
    return opcode + ((rd & 0xF) << 4)


def eicall() -> int:
    return 0x9519


def eijump() -> int:
    return 0x9419

# ToDo: Needs implemtation


def elpm(rd: int) -> int:
    print("Undefinded")
    exit()


def eor(rd: int, rr: int) -> int:
    opcode = 0x2400
    return opcode + twoOp(rd, rr)


def fmul(rd: int, rr: int) -> int:
    opcode = 0x0308
    return opcode + ((rd & 0x7) << 4) + (rr & 0x7)


InstructionsMap = {
    "adc": adc,
    "add": add,
    "adiw": adiw,
    "asr": asr,
    "ldi": ldi,
    "mov": mov,
    "brbc": brbc,
    "brbs": brbs,
    "and": and_,
    "andi": andi
}
