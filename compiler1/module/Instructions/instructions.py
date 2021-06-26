from . import twoOp, twoComplement
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
    opcode = 0x2000
    return opcode + twoOp(rd, rr)


def andi(rd: int, immediate: int) -> int:
    opcode = 0x7000
    kh = (immediate & 0xF0) << 4
    kl = (immediate & 0xF)
    d = (rd & 0xF) << 4
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
    k = twoComplement(rr, 7) << 3
    return opcode + k + s


def brbs(rd: int, rr: int) -> int:
    opcode = 0xF000
    s = rd
    k = twoComplement(rr, 7) << 3
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
    return opcode + ((rd & 0x3E0000) << 3) + (rd & 0x1FFFF)


def cbi(rd: int, rr: int) -> int:
    opcode = 0x9800
    return opcode + (rd << 3) + rr


def cbr(rd: int, rr: int) -> int:
    return andi(rd, rr)


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
    return opcode + twoOp(rd, rd)


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


def elpm() -> int:
    return 0x95D8


def elpmz(rd: int) -> int:
    opcode = 0x9006
    return opcode + (rd << 4)


def elpmzi(rd: int) -> int:
    opcode = 0x9007
    return opcode + (rd << 4)


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


def ijmp() -> int:
    return 0x9409


def in_(rd: int, rr: int) -> int:
    opcode = 0xB000
    return opcode + ((rr & 0x30) << 5) + (rr & 0xF) + ((rd & 0x1F) << 4)


def inc(rd: int) -> int:
    opcode = 0x9403
    return opcode + (rd << 4)


def jmp(rd: int) -> int:
    opcode = 0x940C0000
    return opcode + (rd & 0x1FFFF) + ((rd & 0x3E0000) << 3)


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


def mulsu(rd: int, rr: int) -> int:
    opcode = 0x0300
    return opcode + ((rd & 0x7) << 4) + (rr & 0x7)


def neg(rd: int) -> int:
    opcode = 0x9401
    return opcode + (rd << 4)


def nop() -> int:
    return 0x0000


def or_(rd: int, rr: int) -> int:
    opcode = 0x2800
    return opcode + twoOp(rd, rr)


def ori(rd: int, k: int) -> int:
    opcode = 0x6000
    k = ((k & 0xF0) << 4) + (k & 0x0F)
    return opcode + ((rd & 0xF) << 4) + k


def out(a: int, rr: int) -> int:
    opcode = 0xB800
    a = ((a & 0x30) << 5) + (a & 0xF)
    return opcode + a + (rr << 4)


def pop(rd: int) -> int:
    opcode = 0x900F
    return opcode + (rd << 4)


def push(rr: int) -> int:
    opcode = 0x920F
    return opcode + (rr << 4)


def rcall(k: int) -> int:
    k = 2**12 + k if k < 0 else k
    opcode = 0xD000
    return opcode + k


def ret() -> int:
    return 0x9508


def reti() -> int:
    return 0x9518


def rjump(rd: int) -> int:
    opcode = 0xC000
    return opcode + twoComplement(rd, 12)


def rol(rd: int) -> int:
    return adc(rd, rd)


def ror(rd: int) -> int:
    opcode = 0x9407
    return opcode + (rd << 4)


def sbc(rd: int, rr: int) -> int:
    opcode = 0x0800
    return opcode + twoOp(rd, rr)


def sbci(rd: int, rr: int) -> int:
    opcode = 0x4000
    rd = (rd & 0xF) << 4
    rr = ((rr & 0xF0) << 4) + (rr & 0xF)
    return opcode + rd + rr


def sbi(rd: int, rr: int) -> int:
    opcode = 0x9A00
    return opcode + (rd << 3) + rr


def sbic(rd: int, rr: int) -> int:
    opcode = 0x9900
    return opcode + (rd << 3) + rr


def sbis(rd: int, rr: int) -> int:
    opcode = 0x9B00
    return opcode + (rd << 3) + rr


def sbiw(rd: int, rr: int) -> int:
    opcode = 0x9700
    rr = ((rr & 0x30) << 2) + (rr & 0xF)
    rd = (((rd - 24) // 2) & 0x3) << 4
    return opcode + rd + rr


def sbr(rd: int, rr: int) -> int:
    opcode = 0x6000
    rr = ((rr & 0xF0) << 4) + (rr & 0xF)
    rd = ((rd & 0xF) << 4)
    return opcode + rd + rr


def sbrc(rd: int, rr: int) -> int:
    opcode = 0xFC00
    return opcode + (rd << 4) + rr


def sbrs(rd: int, rr: int) -> int:
    opcode = 0xFE00
    return opcode + (rd << 4) + rr


def sec() -> int:
    return 0x9408


def seh() -> int:
    return 0x9458


def sei() -> int:
    return 0x9478


def sen() -> int:
    return 0x9428


def ser(rd: int) -> int:
    opcode = 0xEF0F
    return opcode + ((rd & 0xF) << 4)


def ses() -> int:
    return 0x9448


def set_() -> int:
    return 0x9468


def sev() -> int:
    return 0x9438


def sez() -> int:
    return 0x9418


def sleep() -> int:
    return 0x9588


def spm() -> int:
    return 0x95E8


def spmz() -> int:
    return 0x95F8


def stx(rd: int) -> int:
    opcode = 0x920C
    return opcode + (rd << 4)


def stxi(rd: int) -> int:
    opcode = 0x920D
    return opcode + (rd << 4)


def stxd(rd: int) -> int:
    opcode = 0x920E
    return opcode + (rd << 4)


def sty(rd: int) -> int:
    opcode = 0x8208
    return opcode + (rd << 4)


def styi(rd: int) -> int:
    opcode = 0x9209
    return opcode + (rd << 4)


def styd(rd: int) -> int:
    opcode = 0x920A
    return opcode + (rd << 4)


def styq(rd: int, rr: int) -> int:
    opcode = 0x8208
    rd = rd << 4
    rr = ((rr & 0x20) << 8) + ((rr & 0x18) << 7) + (rr & 0x7)
    return opcode + rd + rr


def stz(rd: int) -> int:
    opcode = 0x8200
    return opcode + (rd << 4)


def stzi(rd: int) -> int:
    opcode = 0x9201
    return opcode + (rd << 4)


def stzd(rd: int) -> int:
    opcode = 0x9202
    return opcode + (rd << 4)


def stzq(rd: int, rr: int) -> int:
    opcode = 0x8200
    rd = rd << 4
    rr = ((rr & 0x20) << 8) + ((rr & 0x18) << 7) + (rr & 0x7)
    return opcode + rd + rr


def sts32(rd: int, rr: int) -> int:
    opcode = 0x9200_0000
    rr = rr << 20
    return opcode + rr + rd


def sts(rd: int, rr: int) -> int:
    opcode = 0xA800
    rd = ((rd & 0x70) << 4) + (rd & 0xF)
    rr = (rr & 0xF) << 4
    return opcode + rd + rr


def sub(rd: int, rr: int) -> int:
    opcode = 0x1800
    return opcode + twoOp(rd, rr)


def subi(rd: int, rr: int) -> int:
    opcode = 0x5000
    rr = ((rr & 0xF0) << 4) + (rr & 0xF)
    rd = (rd & 0xF) << 4
    return opcode + rr + rd


def swap(rd: int) -> int:
    opcode = 0x9402
    return opcode + (rd << 4)


def tst(rd: int) -> int:
    return and_(rd, rd)


def wdr() -> int:
    return 0x95A8


def xch(rd: int) -> int:
    opcode = 0x9204
    return opcode + (rd << 4)


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
    "andi": andi,
    "lsl": lsl,
    "lsr": lsr,
    "sub": sub,
    "sbc": sbc,
    "subi": subi,
    "sbci": sbci,
    "sbiw": sbiw,
    "push": push,
    "pop": pop
}
