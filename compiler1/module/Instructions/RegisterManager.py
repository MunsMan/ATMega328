from ..Instructions.instructions import mapInstructions
from . import *
from .MemoryManager import MemoryManager
from .helper import getRegister
from typing import Dict, List, Tuple, Union


class RegisterManager:
    _swapMap: Dict[Register, Address] = {}
    registers = [False] * 32

    @staticmethod
    def getFreeRegister(lower=0) -> int:
        for register, state in enumerate(RegisterManager.registers[lower:]):
            if not state:
                RegisterManager.registers[register] = True
                return register
        return -1

    @staticmethod
    def freeRegister(register: Union[str, int]) -> None:
        register = getRegister(register)
        RegisterManager.registers[register] = False

    @staticmethod
    def setRegister(register: Union[str, int]) -> None:
        register = getRegister(register)
        RegisterManager.registers[register] = True

    @staticmethod
    def registerIsUsed(register: Union[str, int]) -> bool:
        register = getRegister(register)
        return RegisterManager.registers[register]

    def getFreeAddressRegister():
        for i, x in enumerate(range(26, 32, 2)):
            r1 = not RegisterManager.registerIsUsed(x)
            r2 = not RegisterManager.registerIsUsed(x + 1)
            if r1 and r2:
                return i
        return -1

    @staticmethod
    def reset():
        RegisterManager.registers = [False] * 32

    #ToDo: Test
    @staticmethod
    def _swapOut(register: int) -> List[Instruction]:
        memoryAddress: Address = MemoryManager.getMemory()
        instruction = mapInstructions("sts")(register, memoryAddress)
        RegisterManager._swapMap[register] = memoryAddress
        return [instruction]

    #ToDo: Test
    @staticmethod
    def _swapIn(register: int) -> List[Instruction]:
        memoryAddress: Address = RegisterManager._swapMap.pop(register)
        instruction = mapInstructions("lds")(register, memoryAddress)
        RegisterManager.setRegister(register)
        MemoryManager.freeMemory(memoryAddress)
        return [instruction]

    @staticmethod
    def getRegister(lower=0) -> Tuple[Register, List[Instruction]]:
        for register, state in enumerate(RegisterManager.registers[lower:]):
            register += lower
            if not state:
                RegisterManager.registers[register] = True
                return getRegister(register), []
        for register in range(lower, 32):
            if not register in RegisterManager._swapMap:
                instructions = RegisterManager._swapOut(register)
                return register, instructions

    @staticmethod
    def returnRegister(register) -> List[Instruction]:
        if register in RegisterManager._swapMap:
            return RegisterManager._swapIn(register)
        RegisterManager.registers[register] = False
        return []
