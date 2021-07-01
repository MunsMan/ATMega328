import pytest
from pytest_mock import MockerFixture
import numpy as np
from ctypes import c_uint8, c_uint16
import random

from .helper import getAllRegisterPointer

from . import mock_exit, bitMask
from .. import helper
from ..helper import *


def test_checkValidConst():
    ks = np.random.randint(0, 255, 1000)
    for k in ks:
        assert checkImmediate('#' + str(k)) == True
        assert checkImmediate(int(k)) == True
        assert checkImmediate(str(k)) == True


def test_checkInvalidConst():
    k = "CONST"
    assert checkImmediate(k) == False


def test_getValidConst(mocker: MockerFixture):
    ks = np.random.randint(0, 255, 1000)
    mock_throwError = mocker.patch.object(helper, "throwError")
    for k in ks:
        assert getImmediate('#' + str(k)) == k
        assert getImmediate(int(k)) == k
        assert getImmediate(str(k)) == k
        assert mock_throwError.call_count == 0


def test_getInvalidConst(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    immediate = "ABC"
    with pytest.raises(SystemExit):
        getImmediate(immediate)
    mock_throwError.assert_called_once_with(6, True, immediate)


def test_checkValidRegister():
    registers = range(0, 32)
    for register in registers:
        assert checkRegister(register) == True
        assert checkRegister('r'+str(register)) == True
        assert checkRegister('R'+str(register)) == True


def test_checkInvalidRegister(mocker: MockerFixture):
    registers = [-1, 32, 'r-1', 'r32', 'R-1',
                 'R32', "ABC", "abc", "d7", "r100"]

    for register in registers:
        assert checkRegister(register) == False


def test_getValidRegister(mocker: MockerFixture):
    registers = range(0, 32)
    mock_throwError = mocker.patch.object(helper, "throwError")
    for register in registers:
        assert getRegister(register) == register
        assert getRegister('r'+str(register)) == register
        assert getRegister('R'+str(register)) == register
        assert mock_throwError.call_count == 0


def test_getInvalidRegister(mocker: MockerFixture):
    registers = [-1, 32, 'r-1', 'r32', 'R-1',
                 'R32', "ABC", "abc", "d7", "r100"]
    mock_throwError = mocker.patch.object(helper, "throwError")
    for register in registers:
        getRegister(register)
        mock_throwError.assert_called_once_with(5, True, register)
        mock_throwError.reset_mock()


def test_getRegisterinBound():
    rds = range(0, 32)
    for rd in rds:
        assert rd == getRegister(f"r{rd}", lower=rd, upper=rd)


def test_getRegisterBoundError(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rds = range(0, 32)
    for rd in rds:
        with pytest.raises(SystemExit):
            getRegister(rd, lower=rd+1)
        mock_throwError.assert_called_once_with(15, True, (rd, rd+1, 31))
        mock_throwError.reset_mock()
        with pytest.raises(SystemExit):
            getRegister(rd, upper=rd-1)
        mock_throwError.assert_called_once_with(15, True, (rd, 0, rd-1))
        mock_throwError.reset_mock()


def test_twoOp():
    mask = "rd dddd rrrr"
    for rd in range(0, 32):
        for rr in range(0, 32):
            expected = bitMask(mask, r=rr, d=rd)
            assert expected == twoOp(rd, rr)


def test_twoComplementValid():
    values = range(-128, 128)
    for value in values:
        assert(twoComplement(value, 8) == c_uint8(value).value)
        assert(twoComplement(value, 16) == c_uint16(value).value)


def test_twoComplementInvalid(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    bit_lengths = range(1, 16)

    for bit_length in bit_lengths:
        toBig = 2**(bit_length-1)
        with pytest.raises(SystemExit):
            twoComplement(toBig, bit_length)
        mock_throwError.assert_called_once_with(10, True, (toBig, bit_length))
        mock_throwError.reset_mock()

        toSmall = -2**(bit_length-1)-1
        with pytest.raises(SystemExit):
            twoComplement(toSmall, bit_length)
        mock_throwError.assert_called_once_with(
            10, True, (toSmall, bit_length))
        mock_throwError.reset_mock()


def test_checkValidRegisterPointer():
    rds = getAllRegisterPointer()
    for rd in rds:
        assert(checkRegisterPointer(rd))


def test_checkInvalidRegisterPointer():
    rds = ['r1', 'A', 'Q', 'r31', 'r0', 'r1-r2']
    for rd in rds:
        assert(not checkRegisterPointer(rd))


def test_getRegisterPointerValid():
    rds = getAllRegisterPointer()
    solutions = range(0, 32)
    for rd in rds:
        result = getRegisterPointer(rd, 0, False)
        assert(result in solutions)


def test_getRegisterPointerInvalidRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rds = ['r1', 'A', 'Q', 'r31', 'r0', 'r1-r2']
    for rd in rds:
        with pytest.raises(SystemExit):
            getRegisterPointer(rd, 0)
        mock_throwError.assert_called_once_with(12, True, rd)
        mock_throwError.reset_mock()


def test_getRegisterPointerLowest(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rds = range(0, 32)
    for rd in rds:
        with pytest.raises(SystemExit):
            args = 'r'+str(rd)+':r'+str(rd+1)
            getRegisterPointer(args, rd+1)
        mock_throwError.assert_called_once_with(11, True, (args, rd+1, False))
        mock_throwError.reset_mock()


def test_getRegisterPointerEven(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rds = range(1, 33, 2)
    for rd in rds:
        with pytest.raises(SystemExit):
            rd = 'r'+str(rd)+':r'+str(rd+1)
            getRegisterPointer(rd, 0, True)
        mock_throwError.assert_called_once_with(11, True, (rd, 0, True))
        mock_throwError.reset_mock()


def test_fromBitMask():
    mask = "11aa bbab ccaa dddd"
    a = 0b01101
    b = 0b000
    c = 0b10
    d = 0b1111
    expected = 0b1101_0010_1001_1111
    result = bitMask(mask, a=a, b=b, c=c, d=d)
    assert(expected == result)


def test_addr():
    addrs = [0, 0xFFFF] + [random.randint(1, 0xFFFE) for i in range(32)]
    addrs = map(hex, addrs)
    for addr in addrs:
        assert Addr.check(addr)
        assert int(addr, base=16) == Addr(addr).value
        assert addr == Addr(addr).hex()
