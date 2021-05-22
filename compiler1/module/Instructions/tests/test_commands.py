from ..instructions import add, and_, andi, ldi
import pytest
from pytest_mock import MockerFixture
from ..commands import ADD, AND, CommandArgs
from .. import commands
from . import mock_exit


def test_addTwoRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("ADD", "", "", 0, 0, None, None, "")

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
    args = CommandArgs("ADD", "", "", None, None, None, None, "")
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
    args = CommandArgs("ADD", "", "", rd, rr, None, None, "")
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(5, True, rd)


def test_addRegisterInvalidRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "r0"
    rr = "r32"
    args = CommandArgs("ADD", "", "", rd, rr, None, None, "")
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(5, True, rr)


def test_andTwoRegister():
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("AND", "", "", None, None, None, None, None)
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
    args = CommandArgs("AND", "", "", None, None, None, None, None)
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
    args = CommandArgs("AND", "", "", None, None, None, None, None)
    for rd in rds:
        for rr in rrs:
            args.rd = 'r' + str(rd)
            args.rr = rr
            numInstructions, instructions = AND(args)
            assert numInstructions == 2
            assert instructions() == [ldi(16, rr), and_(rd, 16)]
