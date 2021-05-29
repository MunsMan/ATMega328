from ..Instructions.branch import *
from . import RegisterManager
from ..errorHandling.error import throwError
from ..Instructions.instructions import mapInstructions
from .helper import checkImmediate, checkImmediateSize, checkRegister, getImmediate, getRegister
from typing import Callable, Union


class CommandArgs:
    def __init__(self, opcode: str, rd: str, rr: str, cond: str = None, flag: str = None, labelRef: Callable = None, lineNum: int = None, label: str = None) -> None:
        self.opcode = opcode
        self.cond = cond
        self.flag = flag
        self.rd = rd
        self.rr = rr
        self.blockIndex = lineNum
        self.label = label
        self.labelRef = lambda: labelRef(
            self.rr if self.rr is not None else self.rd,
            self.blockIndex,
            self.label)


def mapCommmands(args: CommandArgs):
    if args.opcode in CommandsMap:
        return CommandsMap[args.opcode](args)
    throwError(4, True, args.opcode)


def ADD(args: CommandArgs):
    rr = args.rr
    rd = args.rd
    instructions = []
    if not checkRegister(rd):
        throwError(5, True, rd)
    if checkImmediate(rr):
        rr = getImmediate(rr)
        r = RegisterManager.getFreeRegister(16)
        instructions = loadImmediate(r, getImmediate(rr))
        instructions.append(mapInstructions(args.opcode.lower())(rd, r))
        RegisterManager.freeRegister(r)
    else:
        if not checkRegister(rr):
            throwError(5, True, rr)
        instructions.append(mapInstructions(args.opcode.lower())(rd, rr))
    return (len(instructions), lambda: instructions)


def MOV(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    instructions = []
    if not checkRegister(rd):
        throwError(5, True, rd)
    if checkImmediate(rr):
        instructions = loadImmediate(rd, getImmediate(rr))
    else:
        if not checkRegister(rr):
            throwError(5, True, rr)
        instructions.append(mapInstructions("mov")(rd, rr))
    RegisterManager.setRegister(rd)
    return (len(instructions), lambda: instructions)


def BR(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    cond = args.cond
    branch_bit = {
        "BC": BRBC,
        "BS": BRBS
    }
    branch_cond = {
        "EQ": BREQ,
        "NE": BRNE,
        "CS": BRCS,
        "CC": BRCC,
        "SH": BRSH,
        "LO": BRLO,
        "MI": BRMI,
        "PL": BRPL,
        "GE": BRGE,
        "LT": BRLT,
        "HS": BRHS,
        "HC": BRHC,
        "TS": BRTS,
        "TC": BRTC,
        "VS": BRVS,
        "VC": BRVC,
        "IE": BRIE,
        "ID": BRID,
    }
    if cond in branch_bit:
        return branch_bit[cond](rd, rr, args.labelRef)
    if cond in branch_cond:
        return branch_cond[cond](rd, args.labelRef)
    throwError(9, True, (cond))


def AND(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    instructions = []
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd)
    if checkImmediate(rr):
        rr = getImmediate(rr)
        if rd < 16:
            r = RegisterManager.getFreeRegister(16)
            instructions += loadImmediate(r, rr)
            instructions.append(mapInstructions("and")(rd, r))
            RegisterManager.freeRegister(r)
        else:
            instructions.append(mapInstructions("andi")(rd, rr))
    else:
        if not checkRegister(rr):
            throwError(5, True, rr)
        rr = getRegister(rr)
        instructions.append(mapInstructions("and")(rd, rr))
    return (len(instructions), lambda: instructions)


CommandsMap = {
    "ADD": ADD,
    "ADC": ADD,
    "MOV": MOV,
    "BR": BR,
    "AND": AND,
}


def loadImmediate(rd: str, immediate: int):
    instructions = []
    checkImmediateSize(immediate, 8)
    if getRegister(rd) > 15:
        instructions.append(mapInstructions("ldi")(getRegister(rd), immediate))
    else:
        r = RegisterManager.getFreeRegister(16)
        instructions.append(mapInstructions("ldi")(r, immediate))
        instructions.append(mapInstructions("mov")(getRegister(rd), r))
        RegisterManager.freeRegister(r)
    RegisterManager.setRegister(rd)
    return instructions
