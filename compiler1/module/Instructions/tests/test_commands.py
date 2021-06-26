from module.Parser.LineParser import LineParser
from ..instructions import *
import pytest
from pytest_mock import MockerFixture
from ..commands import *
from .. import commands
from .. import helper
from . import mock_exit

invalidRegisters = ["r32", "1", "r-1", "ro", "AB", "-1", "r#"]


def test_movRegisterRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    for rd in rds:
        for rr in rrs:
            args = LineParser(f"MOV r{rd} r{rr}", None, None, None)
            numInstruction, instructions = MOV(args)
            assert(numInstruction == 1)
            assert(instructions() == [mov(rd, rr)])
    mock_throwError.assert_not_called()


def test_movRegisterImmediate(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_getRegister = mocker.patch.object(
        commands.RegisterManager, "getFreeRegister")
    mock_getRegister.return_value = 16
    rds = range(0, 32)
    rrs = range(0, 256)
    # Register < 16
    for rd in rds[:16]:
        for rr in rrs:
            args = LineParser(f"MOV r{rd} {rr}", None, None, None)
            numInstruction, instructions = MOV(args)
            assert(numInstruction == 2)
            assert(instructions() == [ldi(16, rr), mov(rd, 16)])
    # Register >= 16
    for rd in rds[16:]:
        for rr in rrs:
            args = LineParser(f"MOV r{rd} {rr}", None, None, None)
            numInstruction, instructions = MOV(args)
            assert(numInstruction == 1)
            assert(instructions() == [ldi(rd, rr)])
        mock_throwError.assert_not_called()


def test_movInvalidFirstRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit

    arg_list = [LineParser("MOV 1 r0", None, None, None),
                LineParser("MOV r-1 r0", None, None, None),
                LineParser("MOV r32 r0", None, None, None),
                LineParser("MOV -1 r0", None, None, None),
                LineParser("MOV ro r0", None, None, None)]

    for args in arg_list:
        with pytest.raises(SystemExit):
            MOV(args)
        mock_throwError.assert_called_once_with(5, True, args.rd)
        mock_throwError.reset_mock()


def test_movInvalidSecondRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit

    arg_list = [LineParser("MOV r0 r-1", None, None, None),
                LineParser("MOV r0 r32", None, None, None),
                LineParser("MOV r0 -1", None, None, None),
                LineParser("MOV r0 ro", None, None, None)]

    for args in arg_list:
        with pytest.raises(SystemExit):
            MOV(args)
        mock_throwError.assert_called_once_with(5, True, args.rr)
        mock_throwError.reset_mock()


def test_movInvalidImmediate(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit

    args = LineParser("MOV r0 -1", None, None, None)
    with pytest.raises(SystemExit):
        MOV(args)
    mock_throwError.assert_called_once_with(5, True, args.rr)
    mock_throwError.reset_mock()


def test_movInvalidImmediateSize(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rr = 256
    args = LineParser(f"MOV r0 {rr}", None, None, None)
    with pytest.raises(SystemExit):
        MOV(args)
    mock_throwError.assert_called_once_with(
        7, True, (rr, rr.bit_length(), 8))
    mock_throwError.reset_mock()


def test_loadImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(commands, "throwError")
    mock_getRegister = mocker.patch.object(
        commands.RegisterManager, "getFreeRegister")
    mock_getRegister.return_value = 16

    rds = range(0, 32)
    immediates = range(0, 256)

    # Register < 16
    for rd in rds[:16]:
        for immediate in immediates:
            instructions = loadImmediate(rd, immediate)
            expected = [ldi(16, immediate), mov(rd, 16)]
            assert(len(instructions) == 2)
            assert(instructions == expected)

    # Register >= 16
    for rd in rds[16:]:
        for immediate in immediates:
            instructions = loadImmediate(rd, immediate)
            assert(len(instructions) == 1)
            assert(instructions == [ldi(rd, immediate)])
    mocker_throwError.assert_not_called()


def test_loadImmediateInvalidRegister(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit

    immediate = 5

    for rd in invalidRegisters:
        with pytest.raises(SystemExit):
            assert(loadImmediate(rd, immediate) == None)
        mocker_throwError.assert_called_once_with(5, True, rd)
        mocker_throwError.reset_mock()


def test_loadImmediateInvalidImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    mock_getRegister = mocker.patch.object(
        commands.RegisterManager, "getFreeRegister")
    mock_getRegister.return_value = 16

    rds = range(0, 32)
    invalidImmediates = [256, -1]

    for rd in rds:
        for immediate in invalidImmediates:
            with pytest.raises(SystemExit):
                loadImmediate(rd, immediate)
            mocker_throwError.assert_called_once_with(
                7, True, (immediate, immediate.bit_length(), 8))
            mocker_throwError.reset_mock()


def test_ASR():
    rds = range(0, 32)
    rrs = range(0, 8)
    for rd in rds:
        for rr in rrs:
            num = rr if rr != 0 else ""
            args = LineParser(f"ASR r{rd} {num}".strip(), None, None, None)
            numInstructions, instructions = ASR(args)
            numExpected = rr if rr != 0 else 1
            expected = [mapInstructions("asr")(rd)] * numExpected
            assert numExpected == numInstructions
            assert expected == instructions()
