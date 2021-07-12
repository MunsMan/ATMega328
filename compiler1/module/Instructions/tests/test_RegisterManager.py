import pytest
from pytest_mock import MockerFixture

from ..MemoryManager import MemoryManager
from ...Instructions.instructions import mapInstructions
from ..RegisterManager import RegisterManager
from .. import RegisterManager as RM


@pytest.fixture(autouse=True)
def reset_RegisterManager():
    MemoryManager.reset()
    RegisterManager.reset()


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


def test_swapOut(mocker: MockerFixture):
    mock_getMemory = mocker.patch.object(MemoryManager, "getMemory")
    register = 0
    memory_addr = MemoryManager._start
    mock_getMemory.return_value = memory_addr
    instructions = RegisterManager._swapOut(register)
    expected = [mapInstructions("sts")(register, memory_addr)]

    assert expected == instructions
    assert {register: memory_addr} == RegisterManager._swapMap


def test_swapIn(mocker: MockerFixture):
    mock_getMemory = mocker.patch.object(MemoryManager, "getMemory")
    mock_freeMemory = mocker.patch.object(MemoryManager, "freeMemory")
    register = 0
    memory_addr = MemoryManager._start
    mock_getMemory.return_value = memory_addr
    RegisterManager._swapOut(register)

    instructions = RegisterManager._swapIn(register)
    expected = [mapInstructions("lds")(register, memory_addr)]

    assert expected == instructions
    assert {} == RegisterManager._swapMap
    mock_freeMemory.assert_called_once()
