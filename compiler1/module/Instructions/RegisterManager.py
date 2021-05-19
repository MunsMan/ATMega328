from ..Instructions.helper import checkIfRegister, getRegister
from typing import Union


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
        for register in list(RegisterManager.registers.keys())[lower:]:
            if not RegisterManager.registers[register]:
                RegisterManager.registers[register] = True
                return getRegister(register)

    @staticmethod
    def freeRegister(register: Union[str, int]):
        checkIfRegister(register)
        if isinstance(register, int):
            register = "r" + str(register)
        RegisterManager.registers[register] = False

    @staticmethod
    def setRegister(register: Union[str, int]):
        checkIfRegister(register)
        if isinstance(register, int):
            register = "r" + str(register)
        RegisterManager.registers[register] = True