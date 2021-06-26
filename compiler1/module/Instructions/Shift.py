from . import getImmediate, getRegister
from ..Parser import LineParser
from .instructions import mapInstructions
from .RegisterManager import RegisterManager


def shift(args: LineParser):
    rd = getRegister(args.rd)
    rr = getImmediate(args.rr, 3) if args.rr is not None else 1
    opcode = args.opcode.lower()
    instructions = [mapInstructions(opcode)(rd)] * rr
    RegisterManager.setRegister(rd)
    return (len(instructions), lambda: instructions)
