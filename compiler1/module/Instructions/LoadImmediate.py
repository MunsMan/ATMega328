from .instructions import mapInstructions
from .RegisterManager import RegisterManager
from . import checkImmediateSize, getRegister


def loadImmediate(rd: str, immediate: int):
    instructions = []
    checkImmediateSize(immediate, 8)
    if getRegister(rd) > 15:
        instructions.append(mapInstructions("ldi")(getRegister(rd), immediate))
    else:
        r, swapInstructions = RegisterManager.getRegister(16)
        instructions += swapInstructions
        instructions.append(mapInstructions("ldi")(r, immediate))
        instructions.append(mapInstructions("mov")(getRegister(rd), r))
        swapInstructions = RegisterManager.returnRegister(r)
        instructions += swapInstructions
    return instructions
