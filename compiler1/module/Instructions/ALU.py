from .LoadImmediate import loadImmediate
from module.errorHandling.error import throwError
from .instructions import mapInstructions
from . import *
from ..Parser.LineParser import LineParser
from .RegisterManager import RegisterManager


def alu(args: LineParser):
    opcode = args.opcode.lower()
    rd = args.rd
    rr = args.rr
    if checkRegisterPointer(rd):
        if opcode not in ["add", "sub"]:
            throwError(13, True, (opcode.upper(), rd))
        return immediateWord(opcode, rd, getImmediate(rr, 6))
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd)
    if checkImmediate(rr):
        rr = getImmediate(rr)
        return immediate(opcode, rd, rr)
    if not checkRegister(rr):
        throwError(5, True, rr)
    rr = getRegister(rr)
    return register(opcode, rd, rr)


def immediateWord(opcode: str, rd: str, rr: int):
    opcode = opcode[0] + opcode[-1] + "iw"
    rd_p = getRegisterPointer(rd, 24, True)
    instruction = mapInstructions(opcode)(rd_p, rr)
    RegisterManager.setRegister(rd_p)
    RegisterManager.setRegister(rd_p+1)
    return (1, lambda: [instruction])


def immediate(opcode: str, rd: int, rr: int):
    RegisterManager.setRegister(rd)
    immediateOperations = ['and', 'sub', "sbc", "or"]
    if opcode in immediateOperations and rd >= 16:
        return 1, lambda: [mapInstructions(opcode + "i")(rd, rr)]
    else:
        r, instructions = RegisterManager.getRegister(16)
        instructions += loadImmediate(r, rr)
        instructions.append(mapInstructions(opcode)(rd, r))
        instructions += RegisterManager.returnRegister(r)
    return (len(instructions), lambda: instructions)


def register(opcode: str, rd: int, rr: int):
    RegisterManager.setRegister(rd)
    return 1, lambda: [mapInstructions(opcode)(rd, rr)]


def complement(args: LineParser):
    rd = getRegister(args.rd)
    opcode = args.opcode.lower()
    RegisterManager.setRegister(rd)
    return 1, lambda: [mapInstructions(opcode)(rd)]


def MULS(args: LineParser):
    rd = args.rd
    rr = args.rr
    if not checkRegister(rd):
        throwError(5, True, rd)
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd, 16, 31)
    rr = getRegister(rr, 16, 31)
    RegisterManager.setRegister(rd)
    return (1, lambda: [mapInstructions("muls")(rd, rr)])


def MULSU(args: LineParser):
    rd = args.rd
    rr = args.rr
    if not checkRegister(rd):
        throwError(5, True, rd)
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd, 16, 23)
    rr = getRegister(rr, 16, 23)
    RegisterManager.setRegister(rd)
    return (1, lambda: [mapInstructions("mulsu")(rd, rr)])