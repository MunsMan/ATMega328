from typing import Dict, Callable
import ctypes as ct
from error import throwError


def twoOp(Rd, Rn):
    dest = mapRegister(Rd)
    src = mapRegister(Rn)
    return ((src >> 4) << 9) + (dest << 4) + (src & 0xF)


def mov(cond, flag, Rd, Rn, op2) -> int:
    if checkIfConst(Rn):
        return ldi(cond, flag, Rd, Rn, op2)
    else:
        return (0b001011 << 10) + twoOp(Rd, Rn)


def ldi(cond, flag, Rd: str, Rn: str, op2) -> int:
    k = getConst(Rn)
    dest = mapRegister(Rd)
    if dest < 16:
        throwError(6, True, (Rd, "r16-r31"))
    opcode = 0xE000
    kh = (k & 0xF0) << 4
    kl = k & 0xF
    dest = (dest - 16) << 4
    return opcode + kh + dest + kl


def add(cond, flag, Rd, Rn, op2) -> int:
    return (3 << 10) + twoOp(Rd, Rn)


def adiw(cond, flag, Rd: str, Rn, op2) -> int:
    Rd_input = Rd
    Rd: int = _parse16BitReg(Rd)
    if Rd > 4 or Rd < 0:
        throwError(3, True, (Rd_input, 2, "Bit", Rd.bit_length(), "Bit"))
    if int(Rn) < 0 or int(Rn) > 0x40:
        throwError(3, True, (Rd_input, 6, "Bit", int(Rn).bit_length(), "Bit"))
    Rn = int(Rn)
    # 1001 0110 KKdd KKKK
    opcode = (0x96 << 8)  # 38400
    dd = (Rd << 4)  # 16
    KK = ((Rn >> 4) << 6)  # 192
    KKKK = (Rn & 0xF)  # 12
    return opcode + KK + dd + KKKK


def logicalAnd(cond, flag, Rd: str, Rr: str, op2):
    Rd = mapRegister(Rd)
    Rr = mapRegister(Rr)

    opcode = 0x8 << 0xa
    r = (Rr >> 4) << 9
    d = (Rd >> 4) << 8
    dddd = (Rd & 0xF) << 4
    rrrr = Rr & 0xF
    return opcode + r + d + dddd + rrrr


def logicalAndIm(cond, flag, Rd: str, Rr: str, op2):
    rd = mapRegister(Rd)
    k = getConst(Rr)
    opcode = 0x7 << 12
    kh = (k & 0xF0) << 4
    kl = (k & 0xF)
    d = rd << 4
    return opcode + kh + d + kl


def shiftRight(cond, flag, Rd: str, Rr: str, op2):
    opcode = 0x9405
    d = mapRegister(Rd) << 4
    return opcode + d


def clearBitSREG(cond, flag, Rd: str, Rr: str, op2):
    opcode = 0x9488
    s = getConst(Rd, 3) << 4
    return opcode + s


def loadBitT(cond, flag, Rd: str, Rr: str, op2):
    opcode = 0xF800
    rd = mapRegister(Rd) << 4
    b = getConst(Rr, 3)
    return opcode + rd + b


def branchIfBitClear(cond, flag, Rd: str, Rr: str, op2):
    opcode = 0xF400
    s = getConst(Rd, bit_length=3)
    k = getConst(Rr, lower=-64, upper=63) << 3
    return opcode + k + s


def _parse16BitReg(R: str) -> int:
    formats = {
        "X": 1,
        "Y": 2,
        "Z": 3,
        "r27:r26": 1,
        "r29:r28": 2,
        "r31:r30": 3,
    }
    if R in formats:
        return formats[R]
    else:
        return -1


instructions: Dict[str, Callable[[str, str, str, str, str], int]] = {
    "MOV": mov,
    "ADD": add,
    "ADIW": adiw,
    "AND": logicalAnd,
    "ANDI": logicalAndIm,
    "ASR": shiftRight,
    "BCLR": clearBitSREG,
    "BLD": loadBitT,
    "BRBC": branchIfBitClear,
}


def instructionMapping(op: str) -> Callable[[str, str, str, str, str], int]:
    if op not in instructions:
        throwError(4, True, op)
    return instructions[op]


def getConst(c: str, bit_length=8, lower=0, upper=0) -> int:
    if upper == 0:
        upper = (2**bit_length-1)
    try:
        int(c.replace("#", ""))
    except(ValueError) as e:
        throwError(6, True, c.replace("#", ""))
    c = int(c.replace("#", ""))
    if c < lower or c > upper:
        throwError(7, True, ("#{}".format(c), bit_length, c.bit_length()))
    return c


def checkIfConst(r: str):
    return r.find('#') != -1


registerMap = {
    "r0": 0x00,
    "r1": 0x01,
    "r2": 0x02,
    "r3": 0x03,
    "r4": 0x04,
    "r5": 0x05,
    "r6": 0x06,
    "r7": 0x07,
    "r8": 0x08,
    "r9": 0x09,
    "r10": 0x0A,
    "r11": 0x0B,
    "r12": 0x0C,
    "r13": 0x0D,
    "r14": 0x0E,
    "r15": 0x0F,
    "r16": 0x10,
    "r17": 0x11,
    "r18": 0x12,
    "r19": 0x13,
    "r20": 0x14,
    "r21": 0x15,
    "r22": 0x16,
    "r23": 0x17,
    "r24": 0x18,
    "r25": 0x19,
    "r26": 0x1A,
    "r27": 0x1B,
    "r28": 0x1C,
    "r29": 0x1D,
    "r30": 0x1E,
    "r31": 0x1F,


}


def mapRegister(r: str) -> int:
    if r in registerMap:
        return registerMap[r]
    else:
        throwError(5, True, r)
