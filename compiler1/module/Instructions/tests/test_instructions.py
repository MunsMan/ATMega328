from module.Instructions.tests.helper import bitMask
from ..instructions import *
from .. import twoComplement
import random


def test_adc():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0001 11rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == adc(rd, rr)


def test_add():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0000 11rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == add(rd, rr)


def test_adiw():
    rds = range(24, 32, 2)
    rrs = range(0, 64)
    mask = "1001 0110 KKdd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=(rd >> 1), K=rr)
            assert expected == adiw(rd, rr)


def test_and():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0010 00rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == and_(rd, rr)


def test_andi():
    rds = range(16, 32)
    immediates = range(0, 256)
    mask = "0111 KKKK dddd KKKK"
    for rd in rds:
        for immediate in immediates:
            expected = bitMask(mask, d=rd, K=immediate)
            assert expected == andi(rd, immediate)


def test_asr():
    rds = range(0, 32)
    mask = "1001 010d dddd 0101"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == asr(rd)


def test_bclr():
    rds = range(0, 8)
    mask = "1001 0100 1sss 1000"
    for rd in rds:
        expected = bitMask(mask, s=rd)
        assert expected == bclr(rd)


def test_bld():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1111 100d dddd 0bbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, b=rr)
            assert expected == bld(rd, rr)


def test_brbc():
    rds = range(0, 8)
    rrs = range(-64, 64)
    mask = "1111 01kk kkkk ksss"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, k=rr, s=rd)
            assert expected == brbc(rd, rr)


def test_brbs():
    rds = range(0, 8)
    rrs = range(-64, 64)
    mask = "1111 00kk kkkk ksss"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, s=rd, k=rr)
            assert expected == brbs(rd, rr)


def test_bset():
    rds = range(0, 8)
    mask = "1001 0100 0sss 1000"
    for rd in rds:
        expected = bitMask(mask, s=rd)
        assert expected == bset(rd)


def test_bst():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1111 101d dddd 0bbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, b=rr)
            assert expected == bst(rd, rr)


def test_call_64k():
    rds = [0, 65535] + [random.randint(1, 65534) for i in range(64)]
    mask = "1001 010k kkkk 111k kkkk kkkk kkkk kkkk"
    for rd in rds:
        expected = bitMask(mask, k=rd)
        assert expected == call(rd)


def test_call_4m():
    rds = [0, 4194303] + [random.randint(1, 4194302) for i in range(64)]
    mask = "1001 010k kkkk 111k kkkk kkkk kkkk kkkk"
    for rd in rds:
        expected = bitMask(mask, k=rd)
        assert expected == call(rd)


def test_cbi():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1001 1000 AAAA Abbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, A=rd, b=rr)
            assert expected == cbi(rd, rr)


def test_cbr():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "0111 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == cbr(rd, rr)


def test_clc():
    expected = 0b1001_0100_1000_1000
    assert expected == clc()


def test_clh():
    expected = 0b1001_0100_1101_1000
    assert expected == clh()


def test_cli():
    expected = 0b1001_0100_1111_1000
    assert expected == cli()


def test_cln():
    expected = 0b1001_0100_1010_1000
    assert expected == cln()


def test_clr():
    rds = range(0, 32)
    mask = "0010 01rd dddd rrrr"
    for rd in rds:
        expected = bitMask(mask, r=rd, d=rd)
        assert expected == clr(rd)


def test_cls():
    expected = 0b1001_0100_1100_1000
    assert expected == cls()


def test_clt():
    expected = 0b1001_0100_1110_1000
    assert expected == clt()


def test_clv():
    expected = 0b1001_0100_1011_1000
    assert expected == clv()


def test_clz():
    expected = 0b1001_0100_1001_1000
    assert expected == clz()


def test_com():
    rds = range(0, 32)
    mask = "1001 010d dddd 0000"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == com(rd)


def test_cp():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0001 01rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == cp(rd, rr)


def test_cpc():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0000 01rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == cpc(rd, rr)


def test_cpi():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "0011 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == cpi(rd, rr)


def test_cpse():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0001 00rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == cpse(rd, rr)


def test_dec():
    rds = range(0, 32)
    mask = "1001 010d dddd 1010"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == dec(rd)


def test_des():
    rds = range(0, 16)
    mask = "1001 0100 KKKK 1011"
    for rd in rds:
        expected = bitMask(mask, K=rd)
        assert expected == des(rd)


def test_eicall():
    expected = 0b1001_0101_0001_1001
    assert expected == eicall()


def test_eijump():
    expected = 0b1001_0100_0001_1001
    assert expected == eijump()


def test_elpm():
    expected = 0b1001_0101_1101_1000
    assert expected == elpm()


def test_elpmz():
    rds = range(0, 32)
    mask = "1001 000d dddd 0110"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == elpmz(rd)


def test_elpmzi():
    rds = range(0, 30)
    mask = "1001 000d dddd 0111"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == elpmzi(rd)


def test_eor():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0010 01rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, r=rr, d=rd)
            assert expected == eor(rd, rr)


def test_fmul():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_0000_1000
    for rd in rds:
        for rr in rrs:
            result = fmul(rd, rr)
            expected = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == expected)


def test_fmuls():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_1000_0000
    for rd in rds:
        for rr in rrs:
            result = fmuls(rd, rr)
            expected = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == expected)


def test_fmulsu():
    rds = range(16, 24)
    rrs = range(16, 24)
    opcode = 0b0000_0011_1000_1000
    for rd in rds:
        for rr in rrs:
            result = fmulsu(rd, rr)
            expected = opcode + ((rd - 16) << 4) + (rr - 16)
            assert(result == expected)


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
            expected = opcode + (rd << 4) + ((rr & 0x30) << 5) + (rr & 0xF)
            assert(result == expected)


def test_inc():
    rds = range(0, 32)
    opcode = 0b1001_0100_0000_0011
    for rd in rds:
        result = inc(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_jmp():
    rds = [0, 4194303]
    opcode = 0b1001_0100_0000_1100 << 16
    for rd in rds:
        result = jmp(rd)
        expected = opcode + (rd & 0x1FFFF) + ((rd & 0x3E0000) << 20)
        assert(result == expected)


def test_lac():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0110
    for rd in rds:
        result = lac(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_las():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0101
    for rd in rds:
        result = las(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_lat():
    rds = range(0, 32)
    opcode = 0b1001_0010_0000_0111
    for rd in rds:
        result = lat(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldx():
    rds = range(0, 32)
    opcode = 0b1001_0000_0000_1100
    for rd in rds:
        result = ldx(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldxi():
    rds = list(range(0, 26)) + list(range(28, 32))
    opcode = 0b1001_0000_0000_1101
    for rd in rds:
        result = ldxi(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldxd():
    rds = list(range(0, 26)) + list(range(28, 32))
    opcode = 0b1001_0000_0000_1110
    for rd in rds:
        result = ldxd(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldy():
    rds = range(0, 32)
    opcode = 0b1000_0000_0000_1000
    for rd in rds:
        result = ldy(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldyi():
    rds = list(range(0, 28)) + [30, 31]
    opcode = 0b1001_0000_0000_1001
    for rd in rds:
        result = ldyi(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldyd():
    rds = list(range(0, 28)) + [30, 31]
    opcode = 0b1001_0000_0000_1010
    for rd in rds:
        result = ldyd(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_lddy():
    rds = range(0, 32)
    qs = range(0, 64)
    opcode = 0b1000_0000_0000_1000
    for rd in rds:
        for q in qs:
            result = lddy(rd, q)
            expected = opcode + (rd << 4) + ((q & 0b10_0000)
                                             << 8) + ((q & 0b11000) << 7) + (q & 0b111)
            assert(result == expected)


def test_ldz():
    rds = range(0, 32)
    opcode = 0b1000_0000_0000_0000
    for rd in rds:
        result = ldz(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldzi():
    rds = range(0, 30)
    opcode = 0b1001_0000_0000_0001
    for rd in rds:
        result = ldzi(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_ldzd():
    rds = range(0, 30)
    opcode = 0b1001_0000_0000_0010
    for rd in rds:
        result = ldzd(rd)
        expected = opcode + (rd << 4)
        assert(result == expected)


def test_lddz():
    rds = range(0, 32)
    qs = range(0, 64)
    opcode = 0b1000_0000_0000_0000
    for rd in rds:
        for q in qs:
            result = lddz(rd, q)
            expected = opcode + (rd << 4) + ((q & 0b10_0000)
                                             << 8) + ((q & 0b01_1000) << 7) + (q & 0b111)
            assert(result == expected)


def test_lds32():
    rds = range(0, 32)
    ks = [0, 65535]
    mask = "1001 000d dddd 0000 kkkk kkkk kkkk kkkk"
    for rd in rds:
        for k in ks:
            result = lds32(rd, k)
            expected = bitMask(mask, d=rd, k=k)
            assert(result == expected)


def test_lds():
    rds = range(16, 32)
    ks = range(0, 128)
    mask = "1010 0kkk dddd kkkk"
    for rd in rds:
        for k in ks:
            result = lds(rd, k)
            expected = bitMask(mask, d=(rd-16), k=k)
            assert(result == expected)


def test_lpm0():
    mask = "1001 0101 1100 1000"
    assert(lpm0() == bitMask(mask))


def test_lpm():
    rds = range(0, 32)
    mask = "1001 000d dddd 0100"
    for rd in rds:
        result = lpm(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_lpmi():
    rds = range(0, 30)
    mask = "1001 000d dddd 0101"
    for rd in rds:
        result = lpmi(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_lsl():
    # Already tested via addition
    pass


def test_lsr():
    rds = range(0, 32)
    mask = "1001 010d dddd 0110"
    for rd in rds:
        result = lsr(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_movw():
    rds = range(0, 32, 2)
    rrs = range(0, 32, 2)
    mask = "0000 0001 dddd rrrr"
    for rd in rds:
        for rr in rrs:
            result = movw(rd, rr)
            expected = bitMask(mask, d=rd//2, r=rr//2)
            assert(result == expected)


def test_mul():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "1001 11rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            result = mul(rd, rr)
            expected = bitMask(mask, d=rd, r=rr)
            assert(result == expected)


def test_muls():
    rds = range(16, 32)
    rrs = range(16, 32)
    mask = "0000 0010 dddd rrrr"
    for rd in rds:
        for rr in rrs:
            result = muls(rd, rr)
            expected = bitMask(mask, d=(rd-16), r=(rr - 16))
            assert(result == expected)


def test_mulsu():
    rds = range(16, 24)
    rrs = range(16, 24)
    mask = "0000 0011 0ddd 0rrr"
    for rd in rds:
        for rr in rrs:
            result = mulsu(rd, rr)
            expected = bitMask(mask, d=(rd-16), r=(rr - 16))
            assert(result == expected)


def test_neg():
    rds = range(0, 32)
    mask = "1001 010d dddd 0001"
    for rd in rds:
        result = neg(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_nop():
    assert(nop() == 0)


def test_or():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0010 10rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            result = or_(rd, rr)
            expected = bitMask(mask, d=rd, r=rr)
            assert(result == expected)


def test_ori():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "0110 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            result = ori(rd, rr)
            expected = bitMask(mask, d=(rd - 16), K=rr)
            assert(result == expected)


def test_out():
    as_ = range(0, 64)
    rrs = range(0, 32)
    mask = "1011 1AAr rrrr AAAA"
    for a in as_:
        for rr in rrs:
            result = out(a, rr)
            expected = bitMask(mask, A=a, r=rr)
            assert(result == expected)


def test_pop():
    rds = range(0, 32)
    mask = "1001 000d dddd 1111"
    for rd in rds:
        result = pop(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_push():
    rds = range(0, 32)
    mask = "1001 001d dddd 1111"
    for rd in rds:
        result = push(rd)
        expected = bitMask(mask, d=rd)
        assert(result == expected)


def test_rcall():
    ks = [-2048, -1, 2047, 0]
    solutions = [2048, 4095, 2047, 0]
    mask = "1101 kkkk kkkk kkkk"
    for i, k in zip(solutions, ks):
        result = rcall(k)
        expected = bitMask(mask, k=i)
        assert(result == expected)


def test_ret():
    mask = "1001 0101 0000 1000"
    assert(ret() == bitMask(mask))


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
