from . import RegisterManager
from ..errorHandling.error import throwError
from ..Instructions.instructions import mapInstructions
from .helper import checkConst, getConst, getRegister
from typing import Callable, Union

class CommandArgs:
    def __init__(self, opcode: str, cond: str, flag: str, rd: str, rr: str, labelRef: Callable, lineNum: int, label: str) -> None:
        self.opcode = opcode
        self.cond = cond
        self.flag = flag
        self.rd = rd
        self.rr = rr
        self.labelRef = labelRef
        self.blockIndex = lineNum
        self.label = label

    def labelRefArgs(self, offset):
        return offset, self.blockIndex, self.label
         


def mapCommmands(args: CommandArgs):
    if args.opcode in CommandsMap:
        return CommandsMap[args.opcode](args)


def ADD(args: CommandArgs):
    rr = args.rr
    rd = args.rd
    instructions = []
    if checkConst(rr):
        r = RegisterManager.getFreeRegister(16)
        instructions = loadImmediate(r, getConst(rr))
        instructions.append(mapInstructions("add")(rd, r))
        RegisterManager.freeRegister(r)
    else:
        instructions.append(mapInstructions("add")(rd, rr))
    return (len(instructions), lambda: instructions)


def MOV(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    instructions = []
    if checkConst(rr):
        instructions = loadImmediate(rd, getConst(rr))
    else:
        instructions.append(mapInstructions("mov")(rd, rr))
    RegisterManager.setRegister(rd)
    return (len(instructions), lambda: instructions)


def BR(args: CommandArgs):
    rd = args.rd
    rr = args.rr
    labelRef = args.labelRef
    cond = args.cond

    def twoArgs(opcode: str, bit: Union[str, int], offset: Union[str, int]):
        if isinstance(bit, str):
            bit = int(bit)
        LEN_INSTRUCTIONS = 1
        if not str(offset).isdigit():
            return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(bit, labelRef(*args.labelRefArgs(offset)))])
        return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(bit, int(offset))])

    def oneArg(opcode: str, offset: Union[str, int]):
        LEN_INSTRUCTIONS = 1
        if not str(offset).isdigit():
            return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(labelRef(*args.labelRefArgs(offset)))])
        return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(offset)])

    case = {
        "BC": twoArgs("brbc", int(rd), rr),
        "BS": twoArgs("brbs", int(rd), rr),
        "EQ": oneArg("breq", rd),
        "NE": oneArg("brne", rd),
        "CS": oneArg("brcs", rd),
        "CC": oneArg("brcc", rd),
        "SH": oneArg("brsh", rd),
        "LO": oneArg("brlo", rd),
        "MI": oneArg("brmi", rd),
        "PL": oneArg("brpl", rd),
        "GE": oneArg("brge", rd),
        "LT": oneArg("brlt", rd),
        "HS": oneArg("brhs", rd),
        "HC": oneArg("brhc", rd),
        "TS": oneArg("brts", rd),
        "TC": oneArg("brtc", rd),
        "VS": oneArg("brvs", rd),
        "VC": oneArg("brvc", rd),
        "IE": oneArg("brie", rd),
        "ID": oneArg("brid", rd),
    }
    if cond in case:
        return case[cond]
    throwError(9, True, (cond))


CommandsMap = {
    "ADD": ADD,
    "MOV": MOV,
    "BR": BR,
}


def loadImmediate(rd: str, immediate: int):
    instructions = []
    if getRegister(rd) > 15:
        instructions.append(mapInstructions("ldi")(getRegister(rd), immediate))
    else:
        r = RegisterManager.getFreeRegister(16)
        instructions.append(mapInstructions("ldi")(r, immediate))
        instructions.append(mapInstructions("mov")(getRegister(rd), r))
        RegisterManager.freeRegister(r)
    RegisterManager.setRegister(rd)
    return instructions