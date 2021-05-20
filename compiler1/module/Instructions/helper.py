from typing import Union
from ..errorHandling.error import throwError

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


def checkConst(register: Union[str, int]) -> bool:
    if isinstance(register, int):
        return True
    if register.isdigit():
        return True
    return register.find("#") != -1


# ToDo Add a range for an expected Const
def getConst(register: Union[str, int]) -> int:
    if not checkConst(register):
        return throwError(6, True, "0 - 255")

    if not isinstance(register, int):
        register = int(register.replace("#", ""))
    return register


def getRegister(register: Union[str, int]) -> int:
    if isinstance(register, int):
        reg = "r" + str(register)
    else:
        reg = register.lower()
    if reg in RegisterMap:
        return RegisterMap[reg]
    throwError(5, True, register)


def checkIfRegister(register: Union[str, int]) -> bool:
    if isinstance(register, int):
        register = "r" + str(register)
    return register.lower() in RegisterMap


def twoOp(Rd, Rn):
    dest = getRegister(Rd)
    src = getRegister(Rn)
    return ((src & 0x10) << 5) + (dest << 4) + (src & 0xF)
