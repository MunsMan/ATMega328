from typing import List
from .RegisterManager import RegisterManager
from .LoadImmediate import loadImmediate
from ..Parser import LineParser
from . import *
from .instructions import mapInstructions


# ToDo: Need to be tested!
def LOAD(args: LineParser):
    rd = args.rd
    rr = args.rr
    if not checkRegister(rd):
        throwError(5, True, rd)
    RegisterManager.setRegister(rd)

    if Addr.check(rr):
        rr: Addr = Addr(rr)
        instructions = mapInstructions("lds")(rd, rr.value)
        return 1, lambda: [instructions]

    if checkImmediate(rr):
        instructions = loadImmediate(rd, getImmediate(rr))
        return len(instructions), lambda: instructions

    rawPointer: str = rr.replace("+", "").replace("-", "")
    instructions = []
    if checkRegisterPointer(rawPointer):
        if len(rr) == 2:
            if rr[0] == '-':
                instructions.append(mapInstructions(f"ld{rr[1].lower()}d")(rd))
            elif rr[1] == '+':
                instructions.append(mapInstructions(f"ld{rr[0].lower()}i")(rd))
        elif len(rr) == len(rawPointer):
            ptr = getRegisterPointer(rawPointer)
            if checkDirect(rawPointer):
                instructions += loadDirect(rr, rd)
            else:
                instructions += loadIndirect(rr, rd)
        else:
            throwError()
        return len(instructions), lambda: instructions


def checkDirect(rawPointer):
    direct = ['X', 'Y', 'Z', 'r26:r27', 'r28:r29', 'r30:r31']
    return rawPointer in direct


def loadIndirect(ptr: int, rd: int) -> List[int]:
    instructions = []
    r1 = RegisterManager.getFreeRegister()
    r2 = RegisterManager.getFreeRegister()
    instructions.append(mapInstructions("mov")(r1, 26))
    instructions.append(mapInstructions("mov")(r2, 27))
    instructions.append(mapInstructions("mov")(26, ptr))
    instructions.append(mapInstructions("mov")(27, ptr+1))
    instructions.append(mapInstructions("ldx")(rd))
    instructions.append(mapInstructions("mov")(26, r1))
    instructions.append(mapInstructions("mov")(27, r2))
    RegisterManager.freeRegister(r1)
    RegisterManager.freeRegister(r2)
    return instructions


def loadDirect(ptr: int, rd: int) -> List[int]:
    ptrMap = {
        26: 'x',
        28: 'y',
        30: 'z'
    }
    direct = ptrMap[ptr]
    return [mapInstructions(f"ld{direct}")(rd)]
