from . import testlib
from ctypes import POINTER, byref, addressof
from .structs import cpu_t, memory_t, sreg_t

testlib.init_memory.restype = POINTER(memory_t)
testlib.init_cpu.restype = POINTER(cpu_t)


def test_init_cpu():
    memory = testlib.init_memory()
    cpu = testlib.init_cpu(memory)
    print(memory, cpu.contents.memory)
    assert isinstance(cpu.contents.sreg, POINTER(sreg_t))
    assert cpu.contents.PC == 0
    assert cpu.contents.clock_cycles == 0
