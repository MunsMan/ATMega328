from .Types import Register
from ..errorHandling.error import throwError
from .instructions import mapInstructions
from . import getRegister
from typing import List
from ..Parser.LineParser import LineParser


def PUSH(args: LineParser):
    registers = __getRegisters(args.rd)
    instructions = list(map(mapInstructions("push"), registers))
    return len(instructions), lambda: instructions


def __registerRange(rrange: str) -> List[Register]:
    if rrange.count("-") > 1:
        throwError(14, True, rrange)
    lower, upper = rrange.split("-")
    lower = getRegister(lower)
    upper = getRegister(upper)
    if lower <= upper:
        return list(range(lower, upper+1))
    else:
        return list(range(lower, upper-1, -1))


def __getRegisters(rd: str) -> List[Register]:
    registers = []
    rds = rd.split(" ")
    for rd in rds:
        if rd.find("-") != -1:
            registers += __registerRange(rd)
        else:
            registers.append(getRegister(rd))
    return registers


def POP(args: LineParser):
    registers = reversed(__getRegisters(args.rd))
    instructions = list(map(mapInstructions("pop"), registers))
    return len(instructions), lambda: instructions
