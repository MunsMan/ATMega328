import pytest
import random
from ctypes import POINTER, c_int8

from .helper import twoOp
from .. import testlib
from ..structs import memory_t, cpu_t


testlib.init_memory.restype = POINTER(memory_t)
testlib.init_cpu.restype = POINTER(cpu_t)


def create_cpu():
    return testlib.init_cpu(testlib.init_memory())


def destroy_cpu(cpu):
    testlib.destroy_cpu(cpu)


def test_adc():
    pass


def test_add():
    cpu = create_cpu().contents
    print(cpu)
    for i in range(0, 32):
        print(cpu.r[i])
    # for _ in range(64):
    #     rd = random.randint(0, 31)
    #     rr = random.randint(0, 31)
    #     vd = c_int8(random.randint(0, 255))
    #     vr = c_int8(random.randint(0, 255))
    #     cpu.contents.r[rd] = vd.value
    #     cpu.contents.r[rr] = vr.value
    #     instruction = twoOp(0b0010_0000_0000_0000, rd, rr)
    #     testlib.add(cpu, instruction)
    #     assert cpu.contents.r[rd] == c_int8(vd.value + vr.value)
    destroy_cpu(cpu)
