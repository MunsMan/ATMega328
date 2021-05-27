from ..instructions import add, and_, andi, ldi, mov
import pytest
from pytest_mock import MockerFixture
from ..commands import ADD, AND, CommandArgs, MOV, mapCommmands, CommandsMap
from .. import commands
from .. import helper
from . import mock_exit


def test_addTwoRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("ADD", "", "")

    for rd in rds:
        for rr in rrs:
            args.rr = 'r' + str(rr)
            args.rd = 'r' + str(rd)
            numInstructions, instructions = ADD(args)
            assert numInstructions == 1
            assert instructions() == [add(rd, rr)]
    mock_throwError.assert_not_called()


def test_addRegisterConstant(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_getRegister = mocker.patch.object(
        commands.RegisterManager, "getFreeRegister")
    mock_getRegister.return_value = 16

    rds = range(0, 32)
    ks = range(0, 256)
    args = CommandArgs("ADD", "", "")
    for rd in rds:
        for k in ks:
            if rd == 16:
                continue
            args.rd = 'r' + str(rd)
            args.rr = '#' + str(k)
            numInstructions, instructions = ADD(args)
            assert numInstructions == 2
            assert instructions() == [ldi(16, k), add(rd, 16)]
    mock_throwError.assert_not_called()


def test_addInvalidRegisterRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "r32"
    rr = "r0"
    args = CommandArgs("ADD", rd, rr)
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(5, True, rd)


def test_addRegisterInvalidRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "r0"
    rr = "r32"
    args = CommandArgs("ADD", rd, rr)
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(5, True, rr)


def test_andTwoRegister():
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("AND", "", "")
    for rd in rds:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = 'r' + str(rr)
            numInstructions, Instructions = AND(args)
            assert numInstructions == 1
            assert Instructions() == [and_(rd, rr)]


def test_andRegister16Immediate():
    rds = range(16, 32)
    rrs = range(0, 256)
    args = CommandArgs("AND", "", "")
    for rd in rds:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = rr
            numInstructions, instructions = AND(args)
            assert numInstructions == 1
            assert instructions() == [andi(rd, rr)]


def test_andRegister0Immediate(mocker: MockerFixture):
    mock_getRegister = mocker.patch.object(
        commands.RegisterManager, "getFreeRegister")
    mock_getRegister.return_value = 16
    rds = range(0, 16)
    rrs = range(0, 256)
    args = CommandArgs("AND", "", "")
    for rd in rds:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = rr
            numInstructions, instructions = AND(args)
            assert numInstructions == 2
            assert instructions() == [ldi(16, rr), and_(rd, 16)]


def test_movRegisterRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("MOV", "", "")
    for rd in rds:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = 'r' + str(rr)
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
    args = CommandArgs("MOV", "", "")
    # Register < 16
    for rd in rds[:16]:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = rr
            numInstruction, instructions = MOV(args)
            assert(numInstruction == 2)
            assert(instructions() == [ldi(16, rr), mov(rd, 16)])
    # Register >= 16
    for rd in rds[16:]:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = rr
            numInstruction, instructions = MOV(args)
            assert(numInstruction == 1)
            assert(instructions() == [ldi(rd, rr)])
        mock_throwError.assert_not_called()


def test_movInvalidFirstRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit

    arg_list = [CommandArgs("MOV", "1", "r0"),
                CommandArgs("MOV", "r-1", "r0"),
                CommandArgs("MOV", "r32", "r0"),
                CommandArgs("MOV", "-1", "r0"),
                CommandArgs("MOV", "ro", "r0")]

    for args in arg_list:
        with pytest.raises(SystemExit):
            MOV(args)
        mock_throwError.assert_called_once_with(5, True, args.rd)
        mock_throwError.reset_mock()


def test_movInvalidSecondRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit

    arg_list = [CommandArgs("MOV", "r0", "r-1"),
                CommandArgs("MOV", "r0", "r32"),
                CommandArgs("MOV", "r0", "-1"),
                CommandArgs("MOV", "r0", "ro")]

    for args in arg_list:
        with pytest.raises(SystemExit):
            MOV(args)
        mock_throwError.assert_called_once_with(5, True, args.rr)
        mock_throwError.reset_mock()


def test_movInvalidImmediate(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit

    args = CommandArgs("MOV", "r0", -1)
    with pytest.raises(SystemExit):
        MOV(args)
    mock_throwError.assert_called_once_with(6, True, args.rr)
    mock_throwError.reset_mock()


def test_movInvalidImmediateSize(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rr = 256
    args = CommandArgs("MOV", "r0", str(rr))
    with pytest.raises(SystemExit):
        MOV(args)
    mock_throwError.assert_called_once_with(
        7, True, (rr, rr.bit_length(), 8))
    mock_throwError.reset_mock()
