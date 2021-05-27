from .. import helper
from ..helper import checkConst, checkRegister, getConst, getRegister, twoOp
import pytest
from pytest_mock import MockerFixture
import numpy as np
from . import mock_exit


def test_checkValidConst():
    ks = np.random.randint(0, 255, 1000)
    for k in ks:
        assert checkConst('#' + str(k)) == True
        assert checkConst(int(k)) == True
        assert checkConst(str(k)) == True


def test_checkInvalidConst():
    k = "CONST"
    assert checkConst(k) == False


def test_getValidConst(mocker: MockerFixture):
    ks = np.random.randint(0, 255, 1000)
    mock_throwError = mocker.patch.object(helper, "throwError")
    for k in ks:
        assert getConst('#' + str(k)) == k
        assert getConst(int(k)) == k
        assert getConst(str(k)) == k
        assert mock_throwError.call_count == 0


def test_getInvalidConst(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    immediate = "ABC"
    with pytest.raises(SystemExit):
        getConst(immediate)
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


def test_twoOp():
    for rd in range(0, 32):
        for rr in range(0, 32):
            assert twoOp(rd, rr) == ((rr & 0x10) << 5) + (rd << 4) + (rr & 0xF)
