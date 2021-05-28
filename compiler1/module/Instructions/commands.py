from ..Instructions.branch import *
from . import RegisterManager
from ..errorHandling.error import throwError
from ..Instructions.instructions import mapInstructions
from .helper import checkConst, checkImmediateSize, checkRegister, getConst, getRegister
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
        self.labelRef = lambda: labelRef(self.rr, self.blockIndex, self.label)


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
    if checkConst(rr):
        rr = getConst(rr)
        r = RegisterManager.getFreeRegister(16)
        instructions = loadImmediate(r, getConst(rr))
        instructions.append(mapInstructions("add")(rd, r))
        RegisterManager.freeRegister(r)
    else:
        if not checkRegister(rr):
            throwError(5, True, rr)
        instructions.append(mapInstructions("add")(rd, rr))
    return (len(instructions), lambda: instructions)


def MOV(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    instructions = []
    if not checkRegister(rd):
        throwError(5, True, rd)
    if checkConst(rr):
        instructions = loadImmediate(rd, getConst(rr))
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
    case = {
        "BC": BRBC(rd, rr, args.labelRef),
        "BS": BRBS(rd, rr, args.labelRef),
        "EQ": BREQ(rd, args.labelRef),
        "NE": BRNE(rd, args.labelRef),
        "CS": BRCS(rd, args.labelRef),
        "CC": BRCC(rd, args.labelRef),
        "SH": BRSH(rd, args.labelRef),
        "LO": BRLO(rd, args.labelRef),
        "MI": BRMI(rd, args.labelRef),
        "PL": BRPL(rd, args.labelRef),
        "GE": BRGE(rd, args.labelRef),
        "LT": BRLT(rd, args.labelRef),
        "HS": BRHS(rd, args.labelRef),
        "HC": BRHC(rd, args.labelRef),
        "TS": BRTS(rd, args.labelRef),
        "TC": BRTC(rd, args.labelRef),
        "VS": BRVS(rd, args.labelRef),
        "VC": BRVC(rd, args.labelRef),
        "IE": BRIE(rd, args.labelRef),
        "ID": BRID(rd, args.labelRef),
    }
    if cond in case:
        return case[cond]
    throwError(9, True, (cond))


def AND(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    instructions = []
    if not checkRegister(rd):
        throwError(5, True, rd)
    rd = getRegister(rd)
    if checkConst(rr):
        rr = getConst(rr)
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
