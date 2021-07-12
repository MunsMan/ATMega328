import pytest
from pytest_mock import MockerFixture
import random

from ..MemoryManager import MemoryManager
from .. import MemoryManager as MemoryManagerObject
from . import *


@pytest.fixture(autouse=True)
def run_reset():
    MemoryManager.reset()


def test_getMemory():
    for i, expectedAddr in enumerate(range(MemoryManager._start, MemoryManager._end)):
        addr = MemoryManager.getMemory()
        assert expectedAddr == addr
        assert i + 1 == len(MemoryManager.mmap)


def test_getMemoryError(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(MemoryManagerObject, "throwError")
    mock_throwError.side_effect = mock_exit
    for _ in range(MemoryManager._start, MemoryManager._end):
        MemoryManager.getMemory()
    with pytest.raises(SystemExit):
        MemoryManager.getMemory()
    mock_throwError.assert_called_once_with(19, True)


def test_freeMemory():
    memory = []
    for _ in range(MemoryManager._start, MemoryManager._end):
        memory.append(MemoryManager.getMemory())
    while memory:
        addr = random.choice(memory)
        memory.remove(addr)
        MemoryManager.freeMemory(addr)

    assert len(MemoryManager.mmap) == 0


def test_checkAddr():
    addr = MemoryManager.getMemory()
    assert MemoryManager.checkAddress(addr)


def test_memory_full():
    lenMemory = MemoryManager._end - MemoryManager._start
    memory = []
    for _ in range(lenMemory):
        memory.append(MemoryManager.getMemory())
    for _ in range(lenMemory//2):
        addr = random.choice(memory)
        memory.remove(addr)
        MemoryManager.freeMemory(addr)
    for _ in range(lenMemory//2):
        MemoryManager.getMemory()
    assert lenMemory == len(MemoryManager.mmap)
