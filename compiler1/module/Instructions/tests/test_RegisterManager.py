from module.Instructions.MemoryManager import MemoryManager
from ...Instructions.instructions import mapInstructions
from ..RegisterManager import RegisterManager


def test_getRegister():
    RegisterManager.reset()
    for i in range(32):
        register, instructions = RegisterManager.getRegister()
        assert i == register
        assert [] == instructions


def test_getRegisterLower():
    for i in range(32):
        RegisterManager.reset()
        register, instructions = RegisterManager.getRegister(i)
        assert i == register
        assert [] == instructions


def test_getRegisterSwap():
    RegisterManager.registers = [True] * 32
    for i in range(32):
        register, instructions = RegisterManager.getRegister()
        expected = [mapInstructions("sts")(i, MemoryManager._start+i)]
        assert i == register
        assert expected == instructions
    assert 32 == len(RegisterManager._swapMap)
    assert 32 == len(MemoryManager.mmap)


def test_returnRegister():
    RegisterManager.registers = [True] * 32
    for register in range(0, 32):
        instructions = RegisterManager.returnRegister(register)
        assert [] == instructions
    assert all(map(lambda x: not x, RegisterManager.registers))


def test_returnRegisterSwap():
    RegisterManager.registers = [True] * 32
    for register in range(32):
        addr = MemoryManager._start+register
        MemoryManager.mmap.add(addr)
        RegisterManager._swapMap[register] = addr
        expected = [mapInstructions("lds")(register, addr)]
        instructions = RegisterManager.returnRegister(register)
        assert expected == instructions
    assert all(RegisterManager.registers)
    assert {} == RegisterManager._swapMap
