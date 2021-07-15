from typing import List
from .LoadImmediate import loadImmediate
from ..Parser import LineParser
from . import *
from .instructions import mapInstructions
from .RegisterManager import RegisterManager


def LOAD(args: LineParser):
    rd = args.rd
    rr = args.rr
    opcode = args.opcode.lower()
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd)
    RegisterManager.setRegister(rd)

    if Addr.check(rr):
        return fromAddress(opcode, rd, rr)

    if checkImmediate(rr):
        return fromImmediate(rd, rr)

    rawPointer: str = rr.replace("+", "").replace("-", "")
    if checkRegisterPointer(rawPointer):
        return fromRegisterPointer(opcode, rd, rr, rawPointer)


def fromAddress(opcode: str, rd: int, rr: str):
    rr: Addr = Addr(rr)
    suffix = "" if rr.value < 128 else "32"
    instructions = mapInstructions(f"{opcode}s{suffix}")(rd, rr.value)
    return 1, lambda: [instructions]


def fromImmediate(rd: int, rr: str):
    instructions = loadImmediate(rd, getImmediate(rr))
    return len(instructions), lambda: instructions


def fromRegisterPointer(opcode: str, rd: int, rr: str, rawPointer: str):
    instructions = []
    if len(rawPointer) == 1:
        suffix = ""
        if rr[0] == '-':
            suffix = '-'
        elif (rr + " ")[1] == '+':
            suffix == '+'
        elif len(rr) > 1:
            throwError(17, True, (False, rawPointer))
        return 1, lambda: [mapInstructions(
            f"{opcode}{rawPointer.lower()}{suffix}")(rd)]

    if len(rr) != len(rawPointer):
        throwError(17, True, (True, rawPointer))

    if getRegisterPointer(rr) in [26, 28, 30]:
        instructions = loadDirect(opcode, rr, rd)
    else:
        instructions = loadIndirect(opcode, rr, rd)

    return len(instructions), lambda: instructions


def mapAddressRegisterToChar(rptr: str):
    return chr(120 + (rptr - 26) // 2)


def loadIndirect(opcode: str, ptr: int, rd: int) -> List[int]:
    ptr = getRegisterPointer(ptr)
    RegisterManager.returnRegister(rd)
    arp = RegisterManager.getFreeAddressRegister()
    instructions = []

    if ptr % 2 != 0:
        throwError(18, True, ())

    if arp == -1:
        r1, swapInstructions = RegisterManager.getRegister()
        instructions += swapInstructions
        r2, swapInstructions = RegisterManager.getRegister()
        instructions += swapInstructions
        instructions.append(mapInstructions("mov")(r1, 26))
        instructions.append(mapInstructions("mov")(r2, 27))
        instructions.append(mapInstructions("mov")(26, ptr))
        instructions.append(mapInstructions("mov")(27, ptr+1))
        instructions.append(mapInstructions(f"{opcode}x")(rd))
        instructions.append(mapInstructions("mov")(26, r1))
        instructions.append(mapInstructions("mov")(27, r2))
        RegisterManager.returnRegister(r1)
        RegisterManager.returnRegister(r2)
    else:
        instructions.append(mapInstructions("mov")(ptr, 26 + arp * 2))
        instructions.append(mapInstructions("mov")(ptr+1, 26 + arp * 2+1))
        instructions.append(mapInstructions(
            f"ld{mapAddressRegisterToChar(26 + arp * 2)}")(rd))
    RegisterManager.setRegister(rd)
    return instructions


def loadDirect(opcode: str, ptr: int, rd: int) -> List[int]:
    direct = mapAddressRegisterToChar(getRegisterPointer(ptr))
    return [mapInstructions(f"{opcode}{direct}")(rd)]
