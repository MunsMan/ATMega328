from module.Instructions.instructions import pop, push
from module.Instructions.Stack import POP, PUSH, __registerRange, __getRegisters
from pytest_mock import MockerFixture
from ...Parser.LineParser import LineParser
from .. import Stack
from .. import helper as Helper
from . import mock_exit
import pytest

from module import Instructions


def test_registerRange():
    rds = range(0, 32)
    for lower in rds:
        for upper in range(lower, 32):
            result = __registerRange(f"r{lower}-r{upper}")
            expected = list(range(lower, upper+1))
            assert expected == result


def test_registerRangeReverse():
    rds = range(0, 32)
    for lower in rds:
        for upper in range(lower, 32):
            result = __registerRange(f"r{upper}-r{lower}")
            expected = list(range(upper, lower-1, -1))
            assert expected == result


def test_registerRangeNegativ(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Stack, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "r-1-r0"
    with pytest.raises(SystemExit):
        __registerRange(rd)
    mock_throwError.assert_called_once_with(14, True, rd)


def test_registerRangeOutOfRange(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "r0-r32"
    with pytest.raises(SystemExit):
        __registerRange(rd)
    mock_throwError.assert_called_once_with(5, True, "r32")


def test_getRegisters():
    rd = "r1-r4 r0 r5 r10 r15-r30"
    expected = list(range(1, 5)) + [0, 5, 10] + list(range(15, 31))
    assert expected == __getRegisters(rd)


def test_PUSH():
    rd = "{r0-r30 r31}"
    args = LineParser(f"PUSH {rd}", None, None, None)
    numInstructions, instructions = PUSH(args)
    assert 32 == numInstructions
    assert list(map(push, range(0, 32))) == instructions()


def test_POP():
    rd = "{r0-r30 r31}"
    args = LineParser(f"PUSH {rd}", None, None, None)
    numInstructions, instructions = POP(args)
    assert 32 == numInstructions
    assert list(map(pop, range(31, -1, -1))) == instructions()
