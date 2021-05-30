from ..instructions import *
import pytest
from pytest_mock import MockerFixture
from ..commands import ADD, AND, CommandArgs, MOV, loadImmediate
from .. import commands
from .. import helper
from . import mock_exit

invalidRegisters = ["r32", "1", "r-1", "ro", "AB", "-1", "r#"]


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


def test_adc(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rd = "r0"
    rr = "r1"
    args = CommandArgs("ADC", rd, rr)
    numInstruction, instructions = ADD(args)
    assert(numInstruction == 1)
    assert(instructions() == [adc(0, 1)])
    mock_throwError.assert_not_called()


def test_adiw(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = ["r24:r25", "r26:r27", "r28:r29", "r30:r31", "X", "Y", "Z"]
    rrs = range(0, 64)
    args = CommandArgs("ADD", "", "")
    for rd in rds:
        args.rd = rd
        for rr in rrs:
            args.rr = rr

            numInstruction, instructions = ADD(args)
            rd = helper.getRegisterPointer(args.rd)
            assert(numInstruction == 1)
            assert(instructions() == [adiw(rd, rr)])
    mock_throwError.assert_not_called()


def test_adiwInvalidRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    invalidRds = ["r22:", "r23:", "r31:", "r0:"]
    rr = 0
    args = CommandArgs("ADD", "", rr)
    for rd in invalidRds:
        args.rd = rd
        with pytest.raises(SystemExit):
            ADD(args)
        mock_throwError.assert_called_once_with(11, True, (rd, 24, True))
        mock_throwError.reset_mock()


def test_adiwInvalidImmediate(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rd = "X"
    args = CommandArgs("ADD", rd, "")
    # Lower Bound Immediate - negative
    immediate = -1
    args.rr = immediate
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(6, True, immediate)
    mock_throwError.reset_mock()
    # Upper Bound Immediate
    immediate = 64
    args.rr = immediate
    with pytest.raises(SystemExit):
        ADD(args)
    mock_throwError.assert_called_once_with(
        7, True, (immediate, immediate.bit_length(), 6))
    mock_throwError.reset_mock()


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
