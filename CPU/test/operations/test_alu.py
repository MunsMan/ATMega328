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
        numberRd, numberRr = random.sample(list(range(32)), 2)
        rd = c_int8(random.randint(0, 255)).value
        rr = c_int8(random.randint(0, 255)).value
        testlib.setC(byref(cpu)) if c == 1 else testlib.clearC(byref(cpu))
        cpu.r[numberRd] = rd
        cpu.r[numberRr] = rr
        instruction = maskOpcode("0001 11rd dddd rrrr", d=numberRd, r=numberRr)
        testlib.adc(byref(cpu), instruction)
        r = c_int8(rd + rr + c).value
        rd7, rr7, r7 = bit7(rd), bit7(rr), bit7(r)
        h = ((bit3(rd) and bit3(rr)) or (bit3(rd)
             and not bit3(r)) or (not bit3(r) and bit3(rr)))
        v = ((rd7 and rr7 and not r7) or (not rd7 and not rr7 and r7))
        n = r7
        s = v ^ n
        z = r == 0
        c = ((rd7 and rr7) or (not r7 and (rr7 or rd7)))
        assert cpu.r[numberRd] == r
        assert h == testlib.getH(byref(cpu))
        assert s == testlib.getS(byref(cpu))
        assert v == testlib.getV(byref(cpu))
        assert n == testlib.getN(byref(cpu))
        assert z == testlib.getZ(byref(cpu))
        assert c == testlib.getC(byref(cpu))
    destroy_cpu(cpu)


def test_add():
    cpu = create_cpu().contents
    for _ in range(64):
        numberRd, numberRr = random.sample(list(range(32)), 2)
        rd = c_int8(random.randint(0, 255)).value
        rr = c_int8(random.randint(0, 255)).value
        cpu.r[numberRd] = rd
        cpu.r[numberRr] = rr
        instruction = maskOpcode("0010 00rd dddd rrrr", d=numberRd, r=numberRr)
        testlib.add(byref(cpu), instruction)
        r = c_int8(rd + rr).value
        rd7, rr7, r7 = bit7(rd), bit7(rr), bit7(r)
        h = ((bit3(rd) and bit3(rr)) or (bit3(rd) and not bit3(r))
             or (not bit3(r) and bit3(rr)))
        v = ((rd7 and rr7 and not r7) or (not rd7 and not rr7 and r7))
        n = r7
        s = v ^ n
        z = r == 0
        c = ((rd7 and rr7) or (not r7 and (rr7 or rd7)))
        assert cpu.r[numberRd] == r
        assert h == testlib.getH(byref(cpu))
        assert s == testlib.getS(byref(cpu))
        assert v == testlib.getV(byref(cpu))
        assert n == testlib.getN(byref(cpu))
        assert z == testlib.getZ(byref(cpu))
        assert c == testlib.getC(byref(cpu))
    destroy_cpu(cpu)


def test_and():
    cpu = create_cpu().contents
    for _ in range(64):
        numberRd, numberRr = random.sample(list(range(32)), 2)
        rd = c_int8(random.randint(0, 255))
        rr = c_int8(random.randint(0, 255))
        cpu.r[numberRd] = rd.value
        cpu.r[numberRr] = rr.value
        instruction = maskOpcode("0010 00rd dddd rrrr", d=numberRd, r=numberRr)
        testlib.and_(byref(cpu), instruction)
        r = c_int8(rd.value & rr.value).value
        print(f"rd: {rd.value}, rr: {rr.value}, r: {r}")
        assert cpu.r[numberRd] == r
        assert testlib.getS(byref(cpu)) == testlib.getN(
            byref(cpu)) ^ testlib.getV(byref(cpu))
        assert testlib.getV(byref(cpu)) == 0
        assert testlib.getN(byref(cpu)) == bit7(r)
        assert testlib.getZ(byref(cpu)) == (r == 0)
    destroy_cpu(cpu)


def test_sub():
    cpu = create_cpu().contents
    for _ in range(64):
        numberRd, numberRr = random.sample(list(range(32)), 2)
        rd = c_int8(random.randint(0, 255)).value
        rr = c_int8(random.randint(0, 255)).value
        cpu.r[numberRd] = rd
        cpu.r[numberRr] = rr
        instruction = maskOpcode("0001 10rd dddd rrrr", d=numberRd, r=numberRr)
        testlib.sub(byref(cpu), instruction)
        r = c_int8(rd - rr).value
        print(f"{rd} - {rr} = {r}")

        h: bool = (not bit3(rd) and bit3(rr)) or (
            bit3(rr) and bit3(r)) or (bit3(r) and not bit3(rd))
        rd7, rr7, r7 = bit7(rd), bit7(rr), bit7(r)
        v: bool = ((rd7 and not rr7 and not r7) or (not rd7 and rr7 and r7))
        n: bool = bool(r7)
        s: bool = bool(n ^ v)
        z: bool = r == 0
        c: bool = (not rd7 and rr7) or (rr7 and r7) or (r7 and not rd7)

        assert r == cpu.r[numberRd]
        assert h == testlib.getH(byref(cpu))
        assert s == testlib.getS(byref(cpu))
        assert v == testlib.getV(byref(cpu))
        assert n == testlib.getN(byref(cpu))
        assert z == testlib.getZ(byref(cpu))
        assert c == testlib.getC(byref(cpu))
    destroy_cpu(cpu)
