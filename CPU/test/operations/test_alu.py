import pytest
import random
from ctypes import POINTER, byref, c_bool, c_int8

from .helper import maskOpcode, bit3, bit7
from .. import testlib
from ..structs import memory_t, cpu_t


testlib.init_memory.restype = POINTER(memory_t)
testlib.init_cpu.restype = POINTER(cpu_t)
testlib.getH.restype = c_bool
testlib.getS.restype = c_bool
testlib.getV.restype = c_bool
testlib.getN.restype = c_bool
testlib.getZ.restype = c_bool
testlib.getC.restype = c_bool
testlib.getI.restype = c_bool
testlib.getT.restype = c_bool


def create_cpu():
    return testlib.init_cpu(testlib.init_memory())


def destroy_cpu(cpu):
    testlib.destroy_cpu(byref(cpu))


def test_adc():
    cpu = create_cpu().contents
    for _ in range(64):
        c = random.sample([0, 1], 1)[0]
        rd, rr = random.sample(list(range(32)), 2)
        vd = c_int8(random.randint(0, 255))
        vr = c_int8(random.randint(0, 255))
        testlib.setC(byref(cpu)) if c == 1 else testlib.clearC(byref(cpu))
        cpu.r[rd] = vd.value
        cpu.r[rr] = vr.value
        instruction = maskOpcode("0001 11rd dddd rrrr", d=rd, r=rr)
        testlib.adc(byref(cpu), instruction)
        r = c_int8(vd.value + vr.value + c).value
        assert cpu.r[rd] == r
        assert testlib.getH(cpu) == ((bit3(rd) and bit3(rr)) or (
            bit3(rd) and not bit3(r)) or (not bit3(r) and bit3(rr)))
        statusRegister(byref(cpu), vd.value, vr.value, r)
    destroy_cpu(cpu)


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
        r = c_int8(vd.value + vr.value).value
        assert cpu.r[rd] == r
        assert testlib.getH(cpu) == ((bit3(rd) and bit3(rr)) or (
            bit3(rd) and not bit3(r)) or (not bit3(r) and bit3(rr)))
        statusRegister(byref(cpu), vd.value, vr.value, r)
    destroy_cpu(cpu)


def test_and():
    cpu = create_cpu().contents
    for _ in range(64):
        rd, rr = random.sample(list(range(32)), 2)
        vd = c_int8(random.randint(0, 255))
        vr = c_int8(random.randint(0, 255))
        cpu.r[rd] = vd.value
        cpu.r[rr] = vr.value
        instruction = maskOpcode("0010 00rd dddd rrrr", d=rd, r=rr)
        testlib.and_(byref(cpu), instruction)
        r = c_int8(vd.value & vr.value).value
        print(f"rd: {vd.value}, rr: {vr.value}, r: {r}")
        assert cpu.r[rd] == r
        assert testlib.getS(byref(cpu)) == testlib.getN(
            byref(cpu)) ^ testlib.getV(byref(cpu))
        assert testlib.getV(byref(cpu)) == 0
        assert testlib.getN(byref(cpu)) == bit7(r)
        assert testlib.getZ(byref(cpu)) == (r == 0)


def test_sub():
    cpu = create_cpu().contents
    for _ in range(64):
        rd, rr = random.sample(list(range(32)), 2)
        vd = random.randint(0, 255)
        vr = random.randint(0, 255)
        cpu.r[rd] = vd
        cpu.r[rr] = vr
        instruction = maskOpcode("0001 10rd dddd rrrr", d=rd, r=rr)
        testlib.sub(byref(cpu), instruction)
        r = c_int8(vd - vr).value
        assert r == cpu.r[rd]
        h: bool = (not bit3(rd) and bit3(rr)) or (
            bit3(rr) and bit3(r)) or (bit3(r) and not bit3(rd))
        assert h == testlib.getH(cpu)
        statusRegister(cpu, vd, vr, r)


def statusRegister(cpu: cpu_t, rd: int, rr: int, r: int):
    rd7: bool = bit7(rd)
    rr7: bool = bit7(rr)
    r7: bool = bit7(r)
    assert testlib.getV(cpu) == ((rd7 and rr7 and not r7) or (
        not rd7 and not rr7 and r7))
    assert testlib.getN(cpu) == r7
    assert testlib.getS(cpu) == testlib.getN(cpu) ^ testlib.getV(cpu)
    assert testlib.getZ(cpu) == (r == 0)
    assert testlib.getC(cpu) == ((rd7 and rr7) or (not r7 and (rr7 or rd7)))
