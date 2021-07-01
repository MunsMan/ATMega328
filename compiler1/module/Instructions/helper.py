from .RegisterPointer import RegisterPointer
from typing import Union
from ..errorHandling.error import throwError
from .Flags import Flags

RegisterMap = {
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


def checkImmediate(register: Union[str, int]) -> bool:
    if isinstance(register, int):
        return True
    if register.isdigit():
        return True
    return register.find("#") != -1


def getImmediate(register: Union[str, int], bits: int = 8) -> int:
    if not checkImmediate(register):
        throwError(6, True, register)
    if not isinstance(register, int):
        register = int(register.replace("#", ""))
    if register < 0:
        throwError(6, True, register)
    if register > 2**bits-1:
        throwError(7, True, (register, register.bit_length(), bits))
    return register


def getRegister(register: Union[str, int], lower: int = 0, upper: int = 31) -> int:
    if isinstance(register, int):
        reg = "r" + str(register)
    else:
        reg = register.lower()
    if reg in RegisterMap:
        reg = RegisterMap[reg]
        if lower <= reg <= upper:
            return reg
        else:
            throwError(15, True, (reg, lower, upper))
    throwError(5, True, register)


def checkRegister(register: Union[str, int]) -> bool:
    if isinstance(register, int):
        register = "r" + str(register)
    return register.lower() in RegisterMap


def twoOp(Rd, Rn):
    dest = getRegister(Rd)
    src = getRegister(Rn)
    return ((src & 0x10) << 5) + (dest << 4) + (src & 0xF)


def twoComplement(value: int, bit_length: int) -> int:
    MAX = 2**bit_length / 2 - 1
    MIN = -(2**bit_length / 2)
    if value > MAX:
        throwError(10, True, (value, bit_length))
    if value < MIN:
        throwError(10, True, (value, bit_length))
    if value < 0:
        return 2**bit_length + value
    return value


def checkFlag(flag: Union[int, str, Flags]) -> int:
    if isinstance(flag, Flags):
        return flag.value
    return getImmediate(flag, 3)


def checkImmediateSize(immediate: int, bit_length: int):
    if immediate < 0 or immediate.bit_length() > bit_length:
        throwError(7, True, (immediate, immediate.bit_length(), bit_length))


def checkRegisterPointer(register: str):
    if register.find(":") != -1:
        return True
    if register.upper() in RegisterPointer:
        return True
    return False


def getRegisterPointer(register: str, lowest: int = 0, even=False):
    if not checkRegisterPointer(register):
        throwError(12, True, register)
    index = register.find(":")
    if index != -1:
        reg_p = getRegister(register[:index])
    else:
        reg_p = RegisterPointer[register.upper()]
    if even:
        if reg_p < lowest or reg_p % 2:
            throwError(11, True, (register, lowest, True))
    else:
        if reg_p < lowest:
            throwError(11, True, (register, lowest, False))
    return reg_p


class Addr:
    def __init__(self, addr: str) -> None:
        self.value: int = self._cast(addr)

    def _cast(self, addr: str) -> int:
        if not (len(addr) <= 6 and addr[:2] == "0x"):
            throwError(16, True, (addr, 4))
        else:
            try:
                return int(addr, base=16)
            except:
                throwError(16, True, (addr, 4))

    @staticmethod
    def check(addr) -> bool:
        return len(addr) <= 6 and addr[:2] == "0x"

    def hex(self) -> str:
        return hex(self.value)
