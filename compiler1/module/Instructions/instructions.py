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
    return opcode + immediate + ((rd & 0xF) << 4)


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


def fmuls(rd: int, rr: int) -> int:
    opcode = 0x0380
    return opcode + ((rd & 0x7) << 4) + (rr & 0x7)


def fmulsu(rd: int, rr: int) -> int:
    opcode = 0x0388
    return opcode + ((rd & 0x7) << 4) + (rr & 0x7)


def icall() -> int:
    return 0x9509


def ijump() -> int:
    return 0x9409


def in_(rd: int, rr: int) -> int:
    opcode = 0xB000
    return opcode + ((rr & 0x30) << 5) + (rr & 0xF) + ((rd & 0x1F) << 4)


def inc(rd: int) -> int:
    opcode = 0x9403
    return opcode + (rd << 4)


def jmp(rd: int) -> int:
    opcode = 0x940C0000
    return opcode + (rd & 0x1FFFF) + ((rd & 0x3E0000) << 20)


def lac(rd: int) -> int:
    opcode = 0x9206
    return opcode + (rd << 4)


def las(rd: int) -> int:
    opcode = 0x9205
    return opcode + (rd << 4)


def lat(rd: int) -> int:
    opcode = 0x9207
    return opcode + (rd << 4)


# LD rd, X
def ldx(rd: int) -> int:
    opcode = 0x900C
    return opcode + (rd << 4)


# LD rd, X+
def ldxi(rd: int) -> int:
    opcode = 0x900D
    return opcode + (rd << 4)


# LD rd, -X
def ldxd(rd: int) -> int:
    opcode = 0x900E
    return opcode + (rd << 4)


# LD rd, Y
def ldy(rd: int) -> int:
    opcode = 0x8008
    return opcode + (rd << 4)


# LD rd, Y+
def ldyi(rd: int) -> int:
    opcode = 0x9009
    return opcode + (rd << 4)


# LD rd, -Y
def ldyd(rd: int) -> int:
    opcode = 0x900A
    return opcode + (rd << 4)


def lddy(rd: int, q: int) -> int:
    opcode = 0x8008
    rd = rd << 4
    q = ((q & 0x20) << 8) + ((q & 0x18) << 7) + (q & 0x7)
    return opcode + rd + q


def ldz(rd: int) -> int:
    opcode = 0x8000
    return opcode + (rd << 4)


def ldzi(rd: int) -> int:
    opcode = 0x9001
    return opcode + (rd << 4)


def ldzd(rd: int) -> int:
    opcode = 0x9002
    return opcode + (rd << 4)


def lddz(rd: int, q: int) -> int:
    opcode = 0x8000
    rd = (rd << 4)
    q = ((q & 0x20) << 8) + ((q & 0x18) << 7) + (q & 0x7)
    return opcode + rd + q


def lds32(rd: int, k: int) -> int:
    opcode = 0x9000_0000
    return opcode + (rd << 20) + k


def lds(rd: int, k: int) -> int:
    opcode = 0xA000
    return opcode + ((rd & 0xF) << 4) + ((k & 0x70) << 4) + (k & 0xF)


def lpm0() -> int:
    return 0x95C8


def lpm(rd: int) -> int:
    opcode = 0x9004
    return opcode + (rd << 4)


def lpmi(rd: int) -> int:
    opcode = 0x9005
    return opcode + (rd << 4)


def lsl(rd: int) -> int:
    return add(rd, rd)


def lsr(rd: int) -> int:
    opcode = 0x9406
    return opcode + (rd << 4)


def movw(rd: int, rr: int) -> int:
    opcode = 0x0100
    return opcode + ((rd // 2) << 4) + (rr // 2)


def mul(rd: int, rr: int) -> int:
    opcode = 0x9C00
    return opcode + twoOp(rd, rr)


def muls(rd: int, rr: int) -> int:
    opcode = 0x0200
    return opcode + ((rd & 0xF) << 4) + (rr & 0xF)


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
