from typing import Callable
from compiler1.module.errorHandling.error import throwError


def mapInstructions(opcode: str) -> Callable:
    if opcode in InstructionsMap:
        return InstructionsMap[opcode]
    throwError(4, True, (opcode))


def ldi(rd: int, const: int):
    pass


def mov(rd: int, rr: int):
    pass


InstructionsMap = {
    "ldi": ldi,
    "mov": mov
}
