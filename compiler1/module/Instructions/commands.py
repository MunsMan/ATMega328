from .Stack import POP, PUSH
from .LoadImmediate import loadImmediate
from ..Parser.LineParser import LineParser
from ..Instructions.branch import *
from .RegisterManager import RegisterManager
from ..errorHandling.error import throwError
from ..Instructions.instructions import add, mapInstructions
from .helper import *
from typing import List, Tuple
from .Addition import addition


def mapCommmands(args: LineParser):
    if args.opcode in CommandsMap:
        return CommandsMap[args.opcode](args)
    throwError(4, True, args.opcode)


def MOV(args: LineParser):
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


def BR(args: LineParser):
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


# ToDo: Needs to be tested!
def ASR(args: LineParser) -> Tuple[int, List[int]]:
    rd = getRegister(args.rd)
    rr = getImmediate(args.rr, 3) if args.rr is not None else 1
    instructions = [mapInstructions("asr")(rd)] * rr
    RegisterManager.setRegister(rd)
    return (len(instructions), lambda: instructions)


CommandsMap = {
    "ADD": addition,
    "ADC": addition,
    "SUB": addition,
    "SBC": addition,
    "MOV": MOV,
    "BR": BR,
    "AND": addition,
    "ASR": ASR,
    "PUSH": PUSH,
    "POP": POP
}
