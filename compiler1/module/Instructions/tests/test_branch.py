import random
from pytest_mock import MockerFixture
import pytest

from .helper import mock_exit
from ..Branch import BR, BRBS, BRBC
from ..instructions import brbc, brbs, mapInstructions
from .. import helper
from .. import Branch
from ...Parser import LineParser


def test_BRBC_validImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(Branch, "throwError")
    flags = range(0, 8)
    offsets = range(-64, 64)
    for flag in flags:
        for offset in offsets:
            numInstructions, instructions = BRBC(flag, offset, None)
            assert(numInstructions == 1)
            assert(instructions() == [brbc(flag, offset)])
    mocker_throwError.assert_not_called()


def test_BRBC_invalidImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    flags = range(0, 8)
    invalidOffsets = [-65, 64]
    for flag in flags:
        for offset in invalidOffsets:
            with pytest.raises(SystemExit):
                BRBC(flag, offset, None)
            mocker_throwError.assert_called_once_with(
                10, True, (offset, 7))
            mocker_throwError.reset_mock()


def test_BRBC_negativFlag(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    invalidFlags = -1
    validOffset = 1
    with pytest.raises(SystemExit):
        BRBC(invalidFlags, validOffset, None)
    mocker_throwError.assert_called_once_with(
        6, True, invalidFlags)
    mocker_throwError.reset_mock()


def test_BRBC_overflowFlag(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    invalidFlags = 8
    validOffset = 1
    with pytest.raises(SystemExit):
        BRBC(invalidFlags, validOffset, None)
    mocker_throwError.assert_called_once_with(
        7, True, (invalidFlags, invalidFlags.bit_length(), 3))
    mocker_throwError.reset_mock()


def test_BRBS_validImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(Branch, "throwError")
    flags = range(0, 8)
    offsets = range(-64, 64)
    for flag in flags:
        for offset in offsets:
            numInstructions, instructions = BRBS(flag, offset, None)
            assert(numInstructions == 1)
            assert(instructions() == [brbs(flag, offset)])
    mocker_throwError.assert_not_called()


def test_BRBS_invalidImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    flags = range(0, 8)
    invalidOffsets = [-65, 64]
    for flag in flags:
        for offset in invalidOffsets:
            with pytest.raises(SystemExit):
                BRBS(flag, offset, None)
            mocker_throwError.assert_called_once_with(
                10, True, (offset, 7))
            mocker_throwError.reset_mock()


def test_BRBS_negativFlag(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    invalidFlags = -1
    validOffset = 1
    with pytest.raises(SystemExit):
        BRBS(invalidFlags, validOffset, None)
    mocker_throwError.assert_called_once_with(
        6, True, invalidFlags)
    mocker_throwError.reset_mock()


def test_BRBS_overflowFlag(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    invalidFlags = 8
    validOffset = 1
    with pytest.raises(SystemExit):
        BRBS(invalidFlags, validOffset, None)
    mocker_throwError.assert_called_once_with(
        7, True, (invalidFlags, invalidFlags.bit_length(), 3))
    mocker_throwError.reset_mock()


def test_jumpCallAddress():
    rds = [0, 4194303] + [random.randint(1, 4194302) for _ in range(64)]
    opcodes = ["BR", "BL"]
    for rd in rds:
        for opcode in opcodes:
            args = LineParser(f"{opcode} {hex(rd)}", None, None, None)
            numInstructions, instructions = BR(args)
            expected = [mapInstructions(
                "jmp" if opcode == "BR" else "call")(rd)]
            assert 1 == numInstructions
            assert expected == instructions()


def test_jumpCallOffset():
    rds = [-2048, 2047] + [random.randint(-2047, 2046) for _ in range(64)]
    opcodes = ["BR", "BL"]
    for rd in rds:
        for opcode in opcodes:
            args = LineParser(f"{opcode} {rd}", None, None, None)
            numInstructions, instructions = BR(args)
            expected = [mapInstructions(
                "rjmp" if opcode == "BR" else "rcall")(rd)]
            assert 1 == numInstructions
            assert expected == instructions()


def test_jumpCallLabel():
    pass
