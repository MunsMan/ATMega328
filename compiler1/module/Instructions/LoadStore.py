from typing import List
from .LoadImmediate import loadImmediate
from ..Parser import LineParser
from . import *
from .instructions import mapInstructions
from .RegisterManager import RegisterManager


# ToDo: Need to be tested for miss usage!
def LOAD(args: LineParser):
    rd = args.rd
    rr = args.rr
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd)

    if Addr.check(rr):
        rr: Addr = Addr(rr)
        instructions = mapInstructions("lds")(rd, rr.value)
        RegisterManager.setRegister(rd)
        return 1, lambda: [instructions]

    if checkImmediate(rr):
        instructions = loadImmediate(rd, getImmediate(rr))
        RegisterManager.setRegister(rd)
        return len(instructions), lambda: instructions

    rawPointer: str = rr.replace("+", "").replace("-", "")
    instructions = []
    if checkRegisterPointer(rawPointer):
        if len(rr) == 1:
            instructions.append(mapInstructions(f"ld{rr.lower()}")(rd))
        elif len(rr) == 2:
            if rr[0] == '-':
                instructions.append(mapInstructions(f"ld{rr[1].lower()}d")(rd))
            elif rr[1] == '+':
                instructions.append(mapInstructions(f"ld{rr[0].lower()}i")(rd))
        elif len(rr) == len(rawPointer):
            ptr = getRegisterPointer(rawPointer)
            if checkDirect(rawPointer):
                instructions += loadDirect(ptr, rd)
            else:
                instructions += loadIndirect(ptr, rd)
        else:
            throwError()
        RegisterManager.setRegister(rd)
        return len(instructions), lambda: instructions


def checkDirect(rawPointer):
    direct = ['X', 'Y', 'Z', 'r26:r27', 'r28:r29', 'r30:r31']
    return rawPointer in direct


def getFreeAddressRegisterPointer() -> int:
    for i, x in enumerate(range(26, 32, 2)):
        r1 = not RegisterManager.registerIsUsed(x)
        r2 = not RegisterManager.registerIsUsed(x + 1)
        if r1 and r2:
            return i
    return -1


def mapRegisterPointerLower(rptr: str):
    ptrMap = {
        26: 'x',
        28: 'y',
        30: 'z'
    }
    return ptrMap[rptr]


def loadIndirect(ptr: int, rd: int) -> List[int]:
    arp = getFreeAddressRegisterPointer()
    instructions = []

    if ptr % 2 != 0:
        throwError()

    if arp == -1:
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
    else:
        instructions.append(mapInstructions("mov")(ptr, 26 + arp * 2))
        instructions.append(mapInstructions("mov")(ptr+1, 26 + arp * 2+1))
        instructions.append(mapInstructions(
            f"ld{mapRegisterPointerLower(26 + arp * 2)}")(rd))
    return instructions


def loadDirect(ptr: int, rd: int) -> List[int]:
    direct = mapRegisterPointerLower(ptr)
    return [mapInstructions(f"ld{direct}")(rd)]
