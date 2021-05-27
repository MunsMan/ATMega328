from ctypes import c_uint8
from ..instructions import and_, andi, brbs
from .. import twoComplement


def test_and():
    rd = 1
    rr = 16
    expected = 0b0010001000010000  # 8720
    assert expected == and_(rd, rr)


def test_andi():
    rds = range(16, 32)
    immediates = range(0, 256)
    opcode = 0b0111 << 12
    for rd in rds:
        for immediate in immediates:
            k = ((immediate & 0xF0) << 4) + (immediate & 0xF)
            d = rd << 4
            expected = opcode + k + d
            assert expected == andi(rd, immediate)


def test_brbs():
    sregs = range(0, 8)
    offset = range(-64, 64)
    opcode = 0b111100 << 12
    for s in sregs:
        for k in offset:
            result = brbs(s, k)
            k = twoComplement(k, 7) << 3
            expected = opcode + k + s
            assert(expected == result)
