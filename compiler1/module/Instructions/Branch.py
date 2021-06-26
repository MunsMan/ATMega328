from ..Parser.LineParser import LineParser
from ..Instructions.helper import checkFlag
from ..Instructions.instructions import mapInstructions
from typing import Callable, Union
from . import Flags
from ..errorHandling import throwError

INSTRUCTIONS_LEN = 1


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


def BRCC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.C, offset, labelRef)


def BRCS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.C, offset, labelRef)


def BREQ(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.Z, offset, labelRef)


def BRGE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.S, offset, labelRef)


def BRHC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.H, offset, labelRef)


def BRHS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.H, offset, labelRef)


def BRID(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.I, offset, labelRef)


def BRIE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.I, offset, labelRef)


def BRLO(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.C, offset, labelRef)


def BRLT(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.S, offset, labelRef)


def BRMI(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.N, offset, labelRef)


def BRNE(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.Z, offset, labelRef)


def BRPL(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.N, offset, labelRef)


def BRSH(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.C, offset, labelRef)


def BRTC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.T, offset, labelRef)


def BRTS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.T, offset, labelRef)


def BRVC(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBC(Flags.V, offset, labelRef)


def BRVS(offset: Union[str, int], labelRef: Callable[[], int]):
    return BRBS(Flags.V, offset, labelRef)


def BRBC(flag: int, offset: Union[str, int], labelRef: Callable[[], int]):
    flag = checkFlag(flag)
    if not str(offset).replace("-", "").isdigit():
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbc')(
            flag, labelRef())]
    else:
        instruction = mapInstructions('brbc')(flag, offset)
        return INSTRUCTIONS_LEN, lambda: [instruction]


def BRBS(flag: int, offset: Union[str, int], labelRef: Callable[[], int]):
    flag = checkFlag(flag)
    if not str(offset).replace("-", "").isdigit():
        return INSTRUCTIONS_LEN, lambda: [mapInstructions('brbs')(
            flag, labelRef())]
    else:
        instruction = mapInstructions('brbs')(flag, int(offset))
        return INSTRUCTIONS_LEN, lambda: [instruction]
