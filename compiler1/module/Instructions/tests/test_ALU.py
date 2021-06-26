from . import mock_exit
from ..helper import getRegisterPointer
from ..RegisterManager import RegisterManager
from ..instructions import ldi, mapInstructions
from .. import Addition
from ..Addition import addition, complement, immediate, immediateWord, register
from module.Parser.LineParser import LineParser
from pytest_mock import MockerFixture
import pytest
from .. import helper as Helper
import random

ALL_COMMANDS = ["ADD", "ADC", "SUB", "SBC", "AND"]
IMMEDIATE_OPERATIONS = ['AND', 'SUB', "SBC"]
IMMEDIATE_WORD = ["ADD", "SUB"]


def test_additionRegister(mocker: MockerFixture):
    mock_register = mocker.patch.object(Addition, "register")
    mock_throwError = mocker.patch.object(Addition, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    opcodes = ALL_COMMANDS
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                args = LineParser(f"{opcode} r{rd} r{rr}", None, None, None)
                addition(args)
                mock_register.assert_called_once_with(opcode.lower(), rd, rr)
                mock_register.reset_mock()
    mock_throwError.assert_not_called()


def test_additionImmediate(mocker: MockerFixture):
    mock_immediate = mocker.patch.object(Addition, "immediate")
    mock_throwError = mocker.patch.object(Addition, "throwError")
    rds = range(0, 32)
    rrs = [0, 255] + [random.randint(1, 254) for _ in range(0, 64)]
    opcodes = ALL_COMMANDS
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                args = LineParser(f"{opcode} r{rd} #{rr}", None, None, None)
                addition(args)
                mock_immediate.assert_called_once_with(opcode.lower(), rd, rr)
                mock_immediate.reset_mock()
    mock_throwError.assert_not_called()


def test_additionWord(mocker: MockerFixture):
    mock_immediateWord = mocker.patch.object(Addition, "immediateWord")
    mock_throwError = mocker.patch.object(Addition, "throwError")
    rds = ["r24:r25", "r26:r27", "r28:r29", "r30:r31", "X", "Y", "Z"]
    rrs = range(0, 64)
    opcodes = IMMEDIATE_WORD
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                args = LineParser(f"{opcode} {rd} {rr}", None, None, None)
                addition(args)
                mock_immediateWord.assert_called_once_with(
                    opcode.lower(), rd, rr)
                mock_immediateWord.reset_mock()
    mock_throwError.assert_not_called()


def test_register():
    rds = range(0, 32)
    rrs = range(0, 32)
    opcodes = map(str.lower, ALL_COMMANDS)
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                numInstructions, instructions = register(opcode, rd, rr)
                assert 1 == numInstructions
                assert [mapInstructions(opcode)(rd, rr)] == instructions()
                assert RegisterManager.registerIsUsed(rd)


def test_immediateLowRegister(mocker: MockerFixture):
    r = 16
    mock_getFreeRegister = mocker.patch.object(
        RegisterManager, "getFreeRegister")
    mock_getFreeRegister.return_value = r
    rds = range(0, 16)
    rrs = range(0, 256)
    opcodes = map(str.lower, ALL_COMMANDS)
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                numInstructions, instructions = immediate(opcode, rd, rr)
                assert 2 == numInstructions
                assert [ldi(r, rr), mapInstructions(
                    opcode)(rd, r)] == instructions()
                assert RegisterManager.registerIsUsed(rd)
                assert not RegisterManager.registerIsUsed(r)


def test_immediateHighRegisterSub():
    rds = range(16, 32)
    rrs = range(0, 256)
    opcodes = map(str.lower, IMMEDIATE_OPERATIONS)
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                numInstructions, instructions = immediate(opcode, rd, rr)
                assert 1 == numInstructions
                assert [mapInstructions(opcode + 'i')
                        (rd, rr)] == instructions()
                assert RegisterManager.registerIsUsed(rd)


def test_immediateHighRegisterAdd(mocker: MockerFixture):
    mock_getFreeRegister = mocker.patch.object(
        RegisterManager, "getFreeRegister")
    rds = range(16, 32)
    rrs = range(0, 256)
    opcodes = ["add", "adc"]
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                r = 16 if rd != 16 else 17
                mock_getFreeRegister.return_value = r
                numInstructions, instructions = immediate(opcode, rd, rr)
                assert 2 == numInstructions
                assert [ldi(r, rr), mapInstructions(
                    opcode)(rd, r)] == instructions()
                assert RegisterManager.registerIsUsed(rd)
                assert not RegisterManager.registerIsUsed(r)


def test_immediateWord():
    rds = ["r24:r25", "r26:r27", "r28:r29", "r30:r31", "X", "Y", "Z"]
    rrs = range(0, 64)
    opcodes = map(str.lower, IMMEDIATE_WORD)
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                numInstructions, instructions = immediateWord(opcode, rd, rr)
                rd_p = getRegisterPointer(rd)
                assert 1 == numInstructions
                assert [mapInstructions(
                    opcode[0] + opcode[-1] + "iw")(rd_p, rr)] == instructions()
                assert RegisterManager.registerIsUsed(rd_p)
                assert RegisterManager.registerIsUsed(rd_p+1)


def test_invalid_rd(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Addition, "throwError")
    mock_throwError.side_effect = mock_exit
    rds = [-1, 32]
    opcodes = ALL_COMMANDS
    for rd in rds:
        for opcode in opcodes:
            args = LineParser(f"{opcode} r{rd} r0", None, None, None)
            with pytest.raises(SystemExit):
                addition(args)
            mock_throwError.assert_called_once_with(5, True, f"r{rd}")
            mock_throwError.reset_mock()


def test_invalid_rr(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Addition, "throwError")
    mock_throwError.side_effect = mock_exit
    rrs = [-1, 32]
    opcodes = ALL_COMMANDS
    for rr in rrs:
        for opcode in opcodes:
            args = LineParser(f"{opcode} r0 r{rr}", None, None, None)
            with pytest.raises(SystemExit):
                addition(args)
            mock_throwError.assert_called_once_with(5, True, f"r{rr}")
            mock_throwError.reset_mock()


def test_invalid_immediate_for_word(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Helper, "throwError")
    mock_throwError.side_effect = mock_exit
    rr = 64
    opcodes = IMMEDIATE_WORD
    for opcode in opcodes:
        args = LineParser(f"{opcode} X #{rr}", None, None, None)
        with pytest.raises(SystemExit):
            addition(args)
        mock_throwError.assert_called_once_with(
            7, True, (rr, rr.bit_length(), 6))
        mock_throwError.reset_mock()
    rr = -1
    for opcode in opcodes:
        args = LineParser(f"{opcode} X #{rr}", None, None, None)
        with pytest.raises(SystemExit):
            addition(args)
        mock_throwError.assert_called_once_with(6, True, rr)
        mock_throwError.reset_mock()


def test_wrong_argument(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Addition, "throwError")
    mock_throwError.side_effect = mock_exit
    opcodes = ["ADC", "SBC", "AND"]
    for opcode in opcodes:
        args = LineParser(f"{opcode} X 1", None, None, None)
        with pytest.raises(SystemExit):
            addition(args)
        mock_throwError.assert_called_once_with(13, True, (opcode, "X"))
        mock_throwError.reset_mock()


def test_complement():
    rds = range(0, 32)
    opcodes = ["NEG", "COM"]
    for rd in rds:
        for opcode in opcodes:
            args = LineParser(f"{opcode} r{rd}", None, None, None)
            numInstructions, instructions = complement(args)
            expected = [mapInstructions(opcode.lower())(rd)]
            assert 1 == numInstructions
            assert expected == instructions()
            assert RegisterManager.registerIsUsed(rd)
