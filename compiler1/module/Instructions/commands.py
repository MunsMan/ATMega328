from .Shift import shift
from .Stack import POP, PUSH
from .LoadImmediate import loadImmediate
from ..Parser.LineParser import LineParser
from ..Instructions.Branch import BR
from .RegisterManager import RegisterManager
from ..errorHandling.error import throwError
from ..Instructions.instructions import mapInstructions
from .helper import *
from .ALU import addition, complement


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


CommandsMap = {
    "ADD": addition,
    "ADC": addition,
    "AND": addition,
    "ASR": shift,
    "BR": BR,
    "COM": complement,
    "EOR": addition,
    "LSL": shift,
    "LSR": shift,
    "MOV": MOV,
    "NEG": complement,
    "OR": addition,
    "PUSH": PUSH,
    "POP": POP,
    "SBC": addition,
    "SUB": addition,
}
