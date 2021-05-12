from ctypes import *
import numpy
from structs import cpu_t, sr_t, testlib
from alu import _add_flags, _adc_flags, _adiw_flags, _and_flags
import random


def setUp():
    cpu = testlib.initCPU()
    sr = testlib.getSR(cpu)
    return cpu, sr


def cleanUp(cpu):
    testlib.freeCPU(cpu)


def test_twoOpGetRd():
    for i in range(0, 31):
        instruction = c_uint16(i << 4)
        assert testlib.getRd(instruction) == i


def test_twoOpGetRr():
    for i in range(0, 32):
        instruction = c_uint16(((i >> 4) << 9) + (i & 0xF))
        assert testlib.getRr(instruction) == i


def test__add():
    cpu, sr = setUp()
    for i in range(0, 1000):
        a = c_int8(random.randint(-128, 127))
        b = c_int8(random.randint(-128, 127))
        _add_flags(sr, a, b)
        _adc_flags(sr, a, b)
    cleanUp(cpu)


def test__adiw_flags():
    cpu, sr = setUp()
    for i in range(0, 1000):
        a = c_uint16(random.randint(0, 0xFFFF))
        b = c_uint8(random.randint(0, 0xFF))
        _adiw_flags(sr, a, b)
    cleanUp(cpu)


def test__and():
    cpu, sr = setUp()
    for i in range(0, 1000):
        a = c_int8(random.randint(-128, 127))
        b = c_int8(random.randint(-128, 127))
        _and_flags(sr, a, b)
    cleanUp(cpu)
