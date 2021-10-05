from typing import Dict


def bit3(reg: int) -> bool:
    return (reg & (1 << 3)) > 0


def bit7(reg: int) -> bool:
    return bool((reg >> 7) & 1)


def getBitAt(byte: int, index: int):
    return (byte & 1 << index - 1) >> (index - 1)


def maskOpcode(opcode: str, **kwargs: Dict[str, int]):
    charDict = {}
    opcode = opcode.replace(" ", "")
    opcode = opcode.replace("_", "")
    for bit in opcode:
        if not bit.isdigit():
            if bit in charDict:
                charDict[bit] += 1
            else:
                charDict[bit] = 1
    for bit in opcode:
        if not bit.isdigit():
            value = getBitAt(kwargs[bit], charDict[bit])
            charDict[bit] -= 1
            opcode = opcode.replace(bit, str(value), 1)
    return int(opcode, 2)


def twoOp(upcode: int, rd: int, rr: int) -> int:
    return upcode + (rd << 4) + (rr & (1 << 5)) + (rr & 0xF)
