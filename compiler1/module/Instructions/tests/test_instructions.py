from module.Instructions.tests.helper import bitMask
from ..instructions import *
import random
from itertools import chain


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
    mask = "0000 0011 0ddd 1rrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == fmul(rd, rr)


def test_fmuls():
    rds = range(16, 24)
    rrs = range(16, 24)
    mask = "0000 0011 1ddd 0rrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == fmuls(rd, rr)


def test_fmulsu():
    rds = range(16, 24)
    rrs = range(16, 24)
    mask = "0000 0011 1ddd 1rrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == fmulsu(rd, rr)


def test_icall():
    expected = 0b1001_0101_0000_1001
    assert expected == icall()


def test_ijmp():
    expected = 0b1001_0100_0000_1001
    assert expected == ijmp()


def test_in():
    rds = range(0, 32)
    rrs = range(0, 64)
    mask = "1011 0AAd dddd AAAA"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, A=rr)
            assert expected == in_(rd, rr)


def test_inc():
    rds = range(0, 32)
    mask = "1001 010d dddd 0011"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == inc(rd)


def test_jmp():
    rds = [0, 4194303] + [random.randint(1, 4194302) for _ in range(64)]
    mask = "1001 010k kkkk 110k kkkk kkkk kkkk kkkk"
    for rd in rds:
        expected = bitMask(mask, k=rd)
        assert expected == jmp(rd)


def test_lac():
    rds = range(0, 32)
    mask = "1001 001r rrrr 0110"
    for rd in rds:
        expected = bitMask(mask, r=rd)
        assert expected == lac(rd)


def test_las():
    rds = range(0, 32)
    mask = "1001 001r rrrr 0101"
    for rd in rds:
        expected = bitMask(mask, r=rd)
        assert expected == las(rd)


def test_lat():
    rds = range(0, 32)
    mask = "1001 001r rrrr 0111"
    for rd in rds:
        expected = bitMask(mask, r=rd)
        assert expected == lat(rd)


def test_ldx():
    rds = range(0, 32)
    mask = "1001 000d dddd 1100"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldx(rd)


def test_ldxi():
    rds = chain(range(0, 26), range(28, 32))
    mask = "1001 000d dddd 1101"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldxi(rd)


def test_ldxd():
    rds = chain(range(0, 26), range(28, 32))
    mask = "1001 000d dddd 1110"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldxd(rd)


def test_ldy():
    rds = range(0, 32)
    mask = "1000 000d dddd 1000"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldy(rd)


def test_ldyi():
    rds = chain(range(0, 28), range(30, 32))
    mask = "1001 000d dddd 1001"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldyi(rd)


def test_ldyd():
    rds = chain(range(0, 28), range(30, 32))
    mask = "1001 000d dddd 1010"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldyd(rd)


def test_lddy():
    rds = range(0, 32)
    rrs = range(0, 64)
    mask = "10q0 qq0d dddd 1qqq"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, q=rr)
            assert expected == lddy(rd, rr)


def test_ldz():
    rds = range(0, 32)
    mask = "1000 000d dddd 0000"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldz(rd)


def test_ldzi():
    rds = range(0, 30)
    mask = "1001 000d dddd 0001"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldzi(rd)


def test_ldzd():
    rds = range(0, 30)
    mask = "1001 000d dddd 0010"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ldzd(rd)


def test_lddz():
    rds = range(0, 32)
    rrs = range(0, 64)
    mask = "10q0 qq0d dddd 0qqq"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, q=rr)
            assert expected == lddz(rd, rr)


def test_ldi():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "1110 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == ldi(rd, rr)


def test_lds32():
    rds = range(0, 32)
    rrs = [0, 65535]
    mask = "1001 000d dddd 0000 kkkk kkkk kkkk kkkk"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, k=rr)
            assert expected == lds32(rd, rr)


def test_lds():
    rds = range(16, 32)
    rrs = range(0, 128)
    mask = "1010 0kkk dddd kkkk"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=(rd-16), k=rr)
            assert expected == lds(rd, rr)


def test_lpm0():
    expected = 0b1001_0101_1100_1000
    assert expected == lpm0()


def test_lpm():
    rds = range(0, 32)
    mask = "1001 000d dddd 0100"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == lpm(rd)


def test_lpmi():
    rds = range(0, 30)
    mask = "1001 000d dddd 0101"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == lpmi(rd)


def test_lsl():
    rds = range(0, 32)
    mask = "0000 11rd dddd rrrr"
    for rd in rds:
        expected = bitMask(mask, r=rd, d=rd)
        assert expected == lsl(rd)


def test_lsr():
    rds = range(0, 32)
    mask = "1001 010d dddd 0110"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == lsr(rd)


def test_mov():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0010 11rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == mov(rd, rr)


def test_movw():
    rds = range(0, 32, 2)
    rrs = range(0, 32, 2)
    mask = "0000 0001 dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd//2, r=rr//2)
            assert expected == movw(rd, rr)


def test_mul():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "1001 11rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == mul(rd, rr)


def test_muls():
    rds = range(16, 32)
    rrs = range(16, 32)
    mask = "0000 0010 dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == muls(rd, rr)


def test_mulsu():
    rds = range(16, 24)
    rrs = range(16, 24)
    mask = "0000 0011 0ddd 0rrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == mulsu(rd, rr)


def test_neg():
    rds = range(0, 32)
    mask = "1001 010d dddd 0001"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == neg(rd)


def test_nop():
    expected = 0b0000_0000_0000_0000
    assert expected == nop()


def test_or():
    rds = range(0, 32)
    rrs = range(0, 32)
    mask = "0010 10rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == or_(rd, rr)


def test_ori():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "0110 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == ori(rd, rr)


def test_out():
    rds = range(0, 64)
    rrs = range(0, 32)
    mask = "1011 1AAr rrrr AAAA"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, A=rd, r=rr)
            assert expected == out(rd, rr)


def test_pop():
    rds = range(0, 32)
    mask = "1001 000d dddd 1111"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == pop(rd)


def test_push():
    rds = range(0, 32)
    mask = "1001 001d dddd 1111"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == push(rd)


def test_rcall():
    rds = [-2048, -1, 2047, 0] + \
        [random.randint(-2047, 2046) for _ in range(64)]
    mask = "1101 kkkk kkkk kkkk"
    for rd in rds:
        expected = bitMask(mask, k=rd)
        assert expected == rcall(rd)


def test_ret():
    expected = 0b1001_0101_0000_1000
    assert expected == ret()


def test_reti():
    expected = 0b1001_0101_0001_1000
    assert expected == reti()


def test_rjmp():
    rds = range(-2048, 2048)
    mask = "1100 kkkk kkkk kkkk"
    for rd in rds:
        expected = bitMask(mask, k=rd)
        assert expected == rjump(rd)


def test_rol():
    rds = range(32)
    mask = "0001 11rd dddd rrrr"
    for rd in rds:
        expected = bitMask(mask, d=rd, r=rd)
        assert expected == rol(rd)


def test_ror():
    rds = range(32)
    mask = "1001 010d dddd 0111"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ror(rd)


def test_sbc():
    rds = range(32)
    rrs = range(32)
    mask = "0000 10rd dddd rrrr"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, r=rr)
            assert expected == sbc(rd, rr)


def test_sbci():
    rds = range(16, 32)
    rrs = range(0, 255)
    mask = "0100 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == sbci(rd, rr)


def test_sbi():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1001 1010 AAAA Abbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, A=rd, b=rr)
            assert expected == sbi(rd, rr)


def test_sbic():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1001 1001 AAAA Abbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, A=rd, b=rr)
            assert expected == sbic(rd, rr)


def test_sbis():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1001 1011 AAAA Abbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, A=rd, b=rr)
            assert expected == sbis(rd, rr)


def test_sbiw():
    rds = range(24, 32, 2)
    rrs = range(0, 64)
    mask = "1001 0111 KKdd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=(rd - 24)//2, K=rr)
            assert expected == sbiw(rd, rr)


def test_sbr():
    rds = range(16, 32)
    rrs = range(0, 256)
    mask = "0110 KKKK dddd KKKK"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, d=rd, K=rr)
            assert expected == sbr(rd, rr)


def test_sbrc():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1111 110r rrrr 0bbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, r=rd, b=rr)
            assert expected == sbrc(rd, rr)


def test_sbrs():
    rds = range(0, 32)
    rrs = range(0, 8)
    mask = "1111 111r rrrr 0bbb"
    for rd in rds:
        for rr in rrs:
            expected = bitMask(mask, r=rd, b=rr)
            assert expected == sbrs(rd, rr)


def test_sec():
    expected = 0b1001_0100_0000_1000
    assert expected == sec()


def test_seh():
    expected = 0b1001_0100_0101_1000
    assert expected == seh()


def test_sei():
    expected = 0b1001_0100_0111_1000
    assert expected == sei()


def test_sen():
    expected = 0b1001_0100_0010_1000
    assert expected == sen()


def test_ser():
    rds = range(16, 32)
    mask = "1110 1111 dddd 1111"
    for rd in rds:
        expected = bitMask(mask, d=rd)
        assert expected == ser(rd)


def test_ses():
    expected = 0b1001_0100_0100_1000
    assert expected == ses()


def test_set():
    expected = 0b1001_0100_0110_1000
    assert expected == set_()


def test_sev():
    expected = 0b1001_0100_0011_1000
    assert expected == sev()


def test_sez():
    expected = 0b1001_0100_0001_1000
    assert expected == sez()


def test_sleep():
    expected = 0b1001_0101_1000_1000
    assert expected == sleep()


def test_spm():
    expected = 0b1001_0101_1110_1000
    assert expected == spm()
