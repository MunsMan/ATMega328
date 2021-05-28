from ..Instructions.helper import checkImmediateSize, twoComplement
from ..Instructions.instructions import mapInstructions
from typing import Callable, Union
from enum import Enum

INSTRUCTIONS_LEN = 1


class Flag(Enum):
    C = 0
    Z = 1
    N = 2
    V = 3
    S = 4
    H = 5
    T = 6
    I = 7


def BRCC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.C, offset, labelRef)


def BRCS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.C, offset, labelRef)


def BREQ(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.Z, offset, labelRef)


def BRGE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.S, offset, labelRef)


def BRHC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.H, offset, labelRef)


def BRHS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.H, offset, labelRef)


def BRID(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.I, offset, labelRef)


def BRIE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.I, offset, labelRef)


def BRLO(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.C, offset, labelRef)


def BRLT(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.S, offset, labelRef)


def BRMI(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.N, offset, labelRef)


def BRNE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.Z, offset, labelRef)


def BRPL(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.N, offset, labelRef)


def BRSH(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.C, offset, labelRef)


def BRTC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.T, offset, labelRef)


def BRTS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.T, offset, labelRef)


def BRVC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flag.V, offset, labelRef)


def BRVS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flag.V, offset, labelRef)


def BRBC(flag: int, offset: Union[str, int], labelRef: Callable[[], int]):
    if not str(offset).replace("-", "").isdigit():
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbc')(
            flag, labelRef())]
    else:
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbc')(flag, int(offset))]


def BRBS(flag: int, offset: Union[str, int], labelRef: Callable[[], int]):
    checkImmediateSize(flag, 3)
    if not str(offset).replace("-", "").isdigit():
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbs')(
            flag, twoComplement(labelRef(), 7))]
    else:
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbs')(
            flag, twoComplement(int(offset), 7))]
