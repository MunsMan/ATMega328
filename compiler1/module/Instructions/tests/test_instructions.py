from ..instructions import *
from .. import twoComplement


def test_add():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b000011 << 10
    for rd in rds:
        for rr in rrs:
            r = (rr & 0x10) << 5
            ddddd = rd << 4
            rrrr = rr & 0xF
            expected = opcode + r + ddddd + rrrr
            assert(add(rd, rr) == expected)


def test_adc():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b000111 << 10
    for rd in rds:
        for rr in rrs:
            r = (rr & 0x10) << 5
            ddddd = rd << 4
            rrrr = rr & 0xF
            expected = opcode + r + ddddd + rrrr
            assert(adc(rd, rr) == expected)


def test_adiw():
    rds = range(24, 32, 2)
    rrs = range(0, 64)
    opcode = 0b10010110 << 8
    for rd in rds:
        for rr in rrs:
            dd = ((rd - 24) // 2) << 4
            KK = (rr & 0x30) << 2
            KKKK = rr & 0x0F
            expected = opcode + KK + dd + KKKK
            assert(adiw(rd, rr) == expected)


def test_asr():
    rds = range(0, 32)
    opcode = 0b1001010000000101
    for rd in rds:
        result = asr(rd)
        rd <<= 4
        expected = opcode + rd
        assert(result == expected)


def test_bclr():
    rds = range(0, 8)
    opcode = 0b1001010010001000
    for rd in rds:
        result = bclr(rd)
        rd <<= 4
        expected = opcode + rd
        assert(result == expected)


def test_bld():
    rds = range(0, 32)
    rrs = range(0, 8)
    opcode = 0b1111_1000_0000_0000
    for rd in rds:
        for rr in rrs:
            result = bld(rd, rr)
            rd <<= 4
            expected = opcode + rd + rr
            assert(result == expected)


def test_bset():
    rds = range(0, 8)
    opcode = 0b1001_0100_0000_1000
    for rd in rds:
        result = bset(rd)
        rd <<= 4
        expected = opcode + rd
        assert(result == expected)


def test_bst():
    rds = range(0, 32)
    rrs = range(0, 8)
    opcode = 0b1111_1010 << 8
    for rd in rds:
        for rr in rrs:
            result = bst(rd, rr)
            rd <<= 4
            expected = opcode + rd + rr
            assert(result == expected)


def test_mov():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b001011 << 10
    for rd in rds:
        for rr in rrs:
            r = (rr & 0x10) << 5
            ddddd = rd << 4
            rrrr = rr & 0xF
            expected = opcode + r + ddddd + rrrr
            assert(mov(rd, rr) == expected)


def test_ldi():
    registers = range(16, 32)
    immediates = range(0, 256)
    opcode = 0b1110 << 12
    for register in registers:
        for immediate in immediates:
            result = ldi(register, immediate)
            r = (register & 0xF) << 4
            k = ((immediate & 0xF0) << 4) + (immediate & 0x0F)
            expected = opcode + r + k
            assert(result == expected)


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
    opcode = 0b1111 << 12
    for s in sregs:
        for k in offset:
            k = twoComplement(k, 7)
            result = brbs(s, k)
            k <<= 3
            expected = opcode + k + s
            assert(expected == result)


def test_brbc():
    sregs = range(0, 8)
    offset = range(-64, 64)
    opcode = 0b111101 << 10
    for s in sregs:
        for k in offset:
            k = twoComplement(k, 7)
            result = brbc(s, k)
            k <<= 3
            expected = opcode + k + s
            assert(expected == result)


def test_call():
    rds = [0, 1, 2, 65533, 65534, 65535]
    opcode = 0b1001_0100_0000_1110 << 16
    for rd in rds:
        result = call(rd)
        expected = opcode + rd
        assert(result == expected)


def test_cbi():
    rds = range(0, 32)
    rrs = range(0, 8)
    opcode = 0b1001_1000 << 8
    for rd in rds:
        for rr in rrs:
            result = cbi(rd, rr)
            expected = opcode + (rd << 3) + rr
            assert(result == expected)


def test_clc():
    opcode = 0b1001_0100_1000_1000
    assert(clc() == opcode)


def test_clh():
    opcode = 0b1001_0100_1101_1000
    assert(clh() == opcode)


def test_cli():
    opcode = 0b1001_0100_1111_1000
    assert(cli() == opcode)


def test_cln():
    opcode = 0b1001_0100_1010_1000
    assert(cln() == opcode)


def test_clr():
    rds = range(0, 32)
    opcode = 0b0010_0100 << 8
    for rd in rds:
        expected = opcode + rd
        assert(clr(rd) == expected)


def test_cls():
    opcode = 0b1001_0100_1100_1000
    assert(cls() == opcode)


def test_clt():
    opcode = 0b1001_0100_1110_1000
    assert(clt() == opcode)


def test_clv():
    opcode = 0b1001_0100_1011_1000
    assert(clv() == opcode)
