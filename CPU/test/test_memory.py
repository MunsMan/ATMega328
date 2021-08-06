from ctypes import POINTER
from . import testlib
from .structs import memory_t

testlib.init_memory.restype = POINTER(memory_t)


def test_init_memory():
    memory: memory_t = testlib.init_memory()
    assert memory.contents.sram_size != 0
    assert memory.contents.flash_size != 0
    assert memory.contents.sram != None
    assert memory.contents.flash != None
