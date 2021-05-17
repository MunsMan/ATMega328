from compiler1.module.errorHandling.error import throwError
from compiler1.module.Instructions.instructions import mapInstructions
from compiler1.module.Instructions.helper import checkConst, checkIfRegister, getConst, getRegister, loadImmediate
from typing import Callable, Union


class RegisterManager:
    def __init__(self) -> None:
        RegisterManager.registers = {
            "r0": 0x00,
            "r1": False,
            "r2": False,
            "r3": False,
            "r4": False,
            "r5": False,
            "r6": False,
            "r7": False,
            "r8": False,
            "r9": False,
            "r10": False,
            "r11": False,
            "r12": False,
            "r13": False,
            "r14": False,
            "r15": False,
            "r16": False,
            "r17": False,
            "r18": False,
            "r19": False,
            "r20": False,
            "r21": False,
            "r22": False,
            "r23": False,
            "r24": False,
            "r25": False,
            "r26": False,
            "r27": False,
            "r28": False,
            "r29": False,
            "r30": False,
            "r31": False,
        }

    @staticmethod
    def getFreeRegister(lower=0) -> int:
        for register in RegisterManager.registers[lower:]:
            if not register:
                RegisterManager.registers[register] = True
                return getRegister(register)

    def freeRegister(register: Union[str, int]):
        checkIfRegister(register)
        if isinstance(register, int):
            register = "r" + str(register)
        RegisterManager.registers[register] = False

    def setRegister(register: Union[str, int]):
        checkIfRegister(register)
        if isinstance(register, int):
            register = "r" + str(register)
        RegisterManager.registers[register] = True


def mapCommmands(opcode: str, cond: str, flag: str, rd: str, rr: str, labelRef: Callable):
    if opcode in CommandsMap:
        return opcode(cond, flag, rd, rr, labelRef)


def ADD(cond: str, flag: str, rd: str, rr: str, labelRef: Callable):
    instructions = []
    if checkConst(rr):
        r = RegisterManager.getFreeRegister(16)
        instructions = loadImmediate(r, getConst(rr))
        instructions.append(mapInstructions("add")(rd, r))
        RegisterManager.freeRegister(r)
    else:
        instructions.append(mapInstructions("add")(rd, rr))
    return (len(instructions), lambda: instructions)


def MOV(cond: str, flag: str, rd: str, rr: str, labelRef: Callable):
    instructions = []
    if checkConst(rr):
        instructions = loadImmediate(rd, getConst(rr))
    else:
        instructions.append(mapInstructions("mov")(rd, rr))
    RegisterManager.setRegister(rd)
    return (len(instructions), lambda: instructions)


def BR(cond: str, flag: str, rd: str, rr: str, labelRef: Callable):

    def twoArgs(opcode: str, bit: int, offset: Union[str, int]):
        LEN_INSTRUCTIONS = 1
        if not str(offset).isdigit():
            return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(bit, labelRef(offset))])
        return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(bit, offset)])

    def oneArg(opcode: str, offset: Union[str, int]):
        LEN_INSTRUCTIONS = 1
        if not str(offset).isdigit():
            return (LEN_INSTRUCTIONS, lambda: [mapInstructions(opcode)(labelRef(offset))])
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
