import pytest
import random
from ctypes import POINTER, byref, c_int8

from .helper import maskOpcode, twoOp
from .. import testlib
from ..structs import memory_t, cpu_t


testlib.init_memory.restype = POINTER(memory_t)
testlib.init_cpu.restype = POINTER(cpu_t)


def create_cpu():
    return testlib.init_cpu(testlib.init_memory())


def destroy_cpu(cpu):
    testlib.destroy_cpu(byref(cpu))


def test_adc():
    pass


def test_add():
    cpu = create_cpu().contents
    for _ in range(64):
        rd, rr = random.sample(list(range(32)), 2)
        vd = c_int8(random.randint(0, 255))
        vr = c_int8(random.randint(0, 255))
        cpu.r[rd] = vd.value
        cpu.r[rr] = vr.value
        instruction = maskOpcode("0010 00rd dddd rrrr", d=rd, r=rr)
        testlib.add(byref(cpu), instruction)
        assert cpu.r[rd] == c_int8(vd.value + vr.value).value
    destroy_cpu(cpu)
