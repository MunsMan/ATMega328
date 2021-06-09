from module.Instructions.tests.helper import fromBitMask
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


def test_clz():
    opcode = 0b1001_0100_1001_1000
    assert(clz() == opcode)


def test_com():
    rds = range(0, 32)
    opcode = 0b1001_0100 << 8
    for rd in rds:
        result = com(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_cp():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b0001_0100 << 8
    for rd in rds:
        for rr in rrs:
            result = cp(rd, rr)
            expected = opcode + ((rr & 0x10) << 5) + (rd << 4) + (rr & 0xF)
            assert(result == expected)


def test_cpc():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b0000_0100 << 8
    for rd in rds:
        for rr in rrs:
            result = cpc(rd, rr)
            expected = opcode + ((rr & 0x10) << 5) + (rd << 4) + (rr & 0xF)
            assert(result == expected)


def test_cpi():
    rds = range(16, 32)
    rrs = range(0, 256)
    opcode = 0b0011 << 12
    for rd in rds:
        for rr in rrs:
            result = cpi(rd, rr)
            expected = opcode + ((rd - 16) << 4) + \
                ((rr & 0xF0) << 4) + (rr & 0xF)
            assert(result == expected)


def test_cpse():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b0001_0000 << 8
    for rd in rds:
        for rr in rrs:
            result = cpse(rd, rr)
            expected = opcode + ((rr & 0x10) << 5) + (rd << 4) + (rr & 0xF)
            assert(result == expected)


def test_dec():
    rds = range(0, 32)
    opcode = 0b1001_0100_0000_1010
    for rd in rds:
        result = dec(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_des():
    rds = range(0, 16)
    opcode = 0b1001_0100_0000_1011
    for rd in rds:
        result = des(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_eicall():
    opcode = 0b1001_0101_0001_1001
    assert(eicall() == opcode)


def test_eijump():
    opcode = 0b1001_0100_0001_1001
    assert(eijump() == opcode)


def test_eor():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcode = 0b0010_0100 << 8
    for rd in rds:
        for rr in rrs:
            result = eor(rd, rr)
            solution = opcode + twoOp(rd, rr)
            assert(result == solution)


def test_fmul():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_0000_1000
    for rd in rds:
        for rr in rrs:
            result = fmul(rd, rr)
            solution = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == solution)


def test_fmuls():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_1000_0000
    for rd in rds:
        for rr in rrs:
            result = fmuls(rd, rr)
            solution = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == solution)


def test_fmulsu():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_1000_1000
    for rd in rds:
        for rr in rrs:
            result = fmulsu(rd, rr)
            solution = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == solution)


def test_icall():
    opcode = 0b1001_0101_0000_1001
    assert(icall() == opcode)


def test_ijump():
    opcode = 0b1001_0100_0000_1001
    assert(ijump() == opcode)


def test_in():
    rds = range(0, 32)
    rrs = range(0, 64)
    opcode = 0b1011 << 12
    for rd in rds:
        for rr in rrs:
            result = in_(rd, rr)
            solution = opcode + (rd << 4) + ((rr & 0x30) << 5) + (rr & 0xF)
            assert(result == solution)


def test_inc():
    rds = range(0, 32)
    opcode = 0b1001_0100_0000_0011
    for rd in rds:
        result = inc(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_jmp():
    rds = [0, 4194303]
    opcode = 0b1001_0100_0000_1100 << 16
    for rd in rds:
        result = jmp(rd)
        solution = opcode + (rd & 0x1FFFF) + ((rd & 0x3E0000) << 20)
        assert(result == solution)


def test_lac():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0110
    for rd in rds:
        result = lac(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_las():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0101
    for rd in rds:
        result = las(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_lat():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0111
    for rd in rds:
        result = lat(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldx():
    rds = range(0, 32)
    opcode = 0b1001_0000_0000_1100
    for rd in rds:
        result = ldx(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldxi():
    rds = list(range(0, 26)) + list(range(28, 32))
    opcode = 0b1001_0000_0000_1101
    for rd in rds:
        result = ldxi(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldxd():
    rds = list(range(0, 26)) + list(range(28, 32))
    opcode = 0b1001_0000_0000_1110
    for rd in rds:
        result = ldxd(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldy():
    rds = range(0, 32)
    opcode = 0b1000_0000_0000_1000
    for rd in rds:
        result = ldy(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldyi():
    rds = list(range(0, 28)) + [30, 31]
    opcode = 0b1001_0000_0000_1001
    for rd in rds:
        result = ldyi(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldyd():
    rds = list(range(0, 28)) + [30, 31]
    opcode = 0b1001_0000_0000_1010
    for rd in rds:
        result = ldyd(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_lddy():
    rds = range(0, 32)
    qs = range(0, 64)
    opcode = 0b1000_0000_0000_1000
    for rd in rds:
        for q in qs:
            result = lddy(rd, q)
            solution = opcode + (rd << 4) + ((q & 0b10_0000)
                                             << 8) + ((q & 0b11000) << 7) + (q & 0b111)
            assert(result == solution)


def test_ldz():
    rds = range(0, 32)
    opcode = 0b1000_0000_0000_0000
    for rd in rds:
        result = ldz(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldzi():
    rds = range(0, 30)
    opcode = 0b1001_0000_0000_0001
    for rd in rds:
        result = ldzi(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_ldzd():
    rds = range(0, 30)
    opcode = 0b1001_0000_0000_0010
    for rd in rds:
        result = ldzd(rd)
        solution = opcode + (rd << 4)
        assert(result == solution)


def test_lddz():
    rds = range(0, 32)
    qs = range(0, 64)
    opcode = 0b1000_0000_0000_0000
    for rd in rds:
        for q in qs:
            result = lddz(rd, q)
            solution = opcode + (rd << 4) + ((q & 0b10_0000)
                                             << 8) + ((q & 0b01_1000) << 7) + (q & 0b111)
            assert(result == solution)


def test_lds32():
    rds = range(0, 32)
    ks = [0, 65535]
    mask = "1001 000d dddd 0000 kkkk kkkk kkkk kkkk"
    for rd in rds:
        for k in ks:
            result = lds32(rd, k)
            solution = fromBitMask(mask, d=rd, k=k)
            assert(result == solution)


def test_lds():
    rds = range(16, 32)
    ks = range(0, 128)
    mask = "1010 0kkk dddd kkkk"
    for rd in rds:
        for k in ks:
            result = lds(rd, k)
            solution = fromBitMask(mask, d=(rd-16), k=k)
            assert(result == solution)


def test_lpm0():
    mask = "1001 0101 1100 1000"
    assert(lpm0() == fromBitMask(mask))


def test_lpm():
    rds = range(0, 32)
    mask = "1001 000d dddd 0100"
    for rd in rds:
        result = lpm(rd)
        solution = fromBitMask(mask, d=rd)
        assert(result == solution)


def test_lpmi():
    rds = range(0, 30)
    mask = "1001 000d dddd 0101"
    for rd in rds:
        result = lpmi(rd)
        solution = fromBitMask(mask, d=rd)
        assert(result == solution)
