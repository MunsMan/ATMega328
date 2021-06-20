from .instructions import mapInstructions
from .RegisterManager import RegisterManager
from . import checkImmediateSize, getRegister


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
