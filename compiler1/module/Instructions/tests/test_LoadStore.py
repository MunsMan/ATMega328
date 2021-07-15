from pytest_mock import MockerFixture
import random
import pytest

from .. import LoadStore
from ..LoadStore import LOAD
from ..RegisterManager import RegisterManager
from ..instructions import mapInstructions
from ...Parser import LineParser
from .. import helper as Helper
from .helper import mock_exit


def test_loadImmediateDirect():
    rds = range(16, 32)
    rrs = [0, 255] + [random.randint(0, 254) for _ in range(32)]
    for rd in rds:
        for rr in rrs:
            args = LineParser(f"LD r{rd} #{rr}", None, None, None)
            numInstructions, instructions = LOAD(args)
            expected = [mapInstructions("ldi")(rd, rr)]
            assert 1 == numInstructions
            assert expected == instructions()
            assert RegisterManager.registerIsUsed(rd)


def test_loadImmediateIndirect(mocker: MockerFixture):
    mock_getFreeRegister = mocker.patch.object(
        LoadStore.RegisterManager, "getRegister")
    rds = range(0, 16)
    rrs = [0, 255] + [random.randint(0, 254) for _ in range(32)]
    for rd in rds:
        for rr in rrs:
            mock_getFreeRegister.return_value = 16, []
            args = LineParser(f"LD r{rd} #{rr}", None, None, None)
            numInstructions, instructions = LOAD(args)
            expected = [mapInstructions("ldi")(
                16, rr), mapInstructions("mov")(rd, 16)]
            assert len(expected) == numInstructions
            assert expected == instructions()
            assert RegisterManager.registerIsUsed(rd)
            assert not RegisterManager.registerIsUsed(16)


def test_loadAddress():
    rds = range(0, 32)
    rrs = [0, 65535] + [random.randint(1, 65534) for _ in range(62)]
    for rd in rds:
        for rr in rrs:
            args = LineParser(f"LD r{rd} {hex(rr)}", None, None, None)
            numInstructions, instructions = LOAD(args)
            expected = [mapInstructions("lds")(rd, rr)]
            assert len(expected) == numInstructions
            assert expected == instructions()
            assert RegisterManager.registerIsUsed(rd)


def mapRegisterPointer(rptr: str) -> str:
    rptrMap = {
        26: 'x',
        28: 'y',
        30: 'z'
    }
    if rptr.find(":") != -1:
        return rptrMap[int(rptr.split(":")[0].replace("r", ""))]
    else:
        return rptr.lower()


def test_registerPointerDirect():
    rds = range(0, 32)
    rrs = ['X', 'Y', 'Z'] + \
        list(map(lambda x: f"r{x}:r{x+1}", range(26, 32, 2)))
    for rd in rds:
        for rr in rrs:
            args = LineParser(f"LD r{rd} {rr}", None, None, None)
            numInstructions, instructions = LOAD(args)
            expectecd = [mapInstructions(f"ld{mapRegisterPointer(rr)}")(rd)]
            assert len(expectecd) == numInstructions
            assert expectecd == instructions()
            assert RegisterManager.registerIsUsed(rd)


lowerRegisterPointerMap = {
    0: 'x',
    1: 'y',
    2: 'z'
}


def test_registerPointerIndirectFree():
    RegisterManager.reset()
    rds = range(0, 32)
    rptrs = range(0, 26, 2)
    for i in range(0, 2):
        for rd in rds:
            for rptr in rptrs:
                for x in range(i):
                    RegisterManager.setRegister(26+x*2)
                    RegisterManager.setRegister(26+x*2+1)
                args = LineParser(
                    f"LD r{rd} r{rptr}:r{rptr+1}", None, None, None)
                numInstructions, instructions = LOAD(args)
                expected = [
                    mapInstructions("mov")(rptr, 26+i*2),
                    mapInstructions("mov")(rptr+1, 26+i*2+1),
                    mapInstructions(f"ld{lowerRegisterPointerMap[i]}")(rd)
                ]
                assert len(expected) == numInstructions
                assert expected == instructions()
                assert RegisterManager.registerIsUsed(rd)
                RegisterManager.freeRegister(rd)


def test_registerPointerIndirectUsed(mocker: MockerFixture):
    RegisterManager.reset()
    mock_getFreeAddressRegisterPointer = mocker.patch.object(
        RegisterManager, "getFreeAddressRegister")
    mock_getFreeAddressRegisterPointer.return_value = -1
    rds = range(0, 32)
    rptrs = range(0, 26, 2)
    for rd in rds:
        for rptr in rptrs:
            RegisterManager.reset()
            args = LineParser(
                f"LD r{rd} r{rptr}:r{rptr+1}", None, None, None)
            numInstructions, instructions = LOAD(args)
            expected = [
                mapInstructions("mov")(0, 26),
                mapInstructions("mov")(1, 27),
                mapInstructions("mov")(26, rptr),
                mapInstructions("mov")(27, rptr+1),
                mapInstructions("ldx")(rd),
                mapInstructions("mov")(26, 0),
                mapInstructions("mov")(27, 1),
            ]
            assert len(expected) == numInstructions
            assert expected == instructions()
            assert RegisterManager.registerIsUsed(rd)
            assert not RegisterManager.registerIsUsed(0) or 0 == rd
            assert not RegisterManager.registerIsUsed(1) or 1 == rd


def test_LoadInvalidAddress(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Helper, "throwError")
    mock_throwError.side_effect = mock_exit
    invalidAddresses = ["0xGGGG", "0x12345"]
    for rr in invalidAddresses:
        args = LineParser(f"LD r0 {rr}", None, None, None)
        with pytest.raises(SystemExit):
            LOAD(args)
        mock_throwError.assert_called_once_with(
            16, True, (rr, 4))
        mock_throwError.reset_mock()


def test_LoadInvalidImmediate(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(Helper, "throwError")
    mock_throwError.side_effect = mock_exit
    invalidImmediate = 0b1_1111_1111
    args = LineParser(f"LD r0 {invalidImmediate}", None, None, None)
    with pytest.raises(SystemExit):
        LOAD(args)
    mock_throwError.assert_called_once_with(7, True, (invalidImmediate, 9, 8))


def test_LoadRegisterPointerOperation(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(LoadStore, "throwError")
    mock_throwError.side_effect = mock_exit
    rawPointers = ["X", "Y", "Z"]
    for rawPointer in rawPointers:

        args = LineParser(f"LD r0 {rawPointer}-", None, None, None)
        with pytest.raises(SystemExit):
            LOAD(args)
        mock_throwError.assert_called_once_with(17, True, (False, rawPointer))
        mock_throwError.reset_mock()

        args = LineParser(f"LD r0 +{rawPointer}", None, None, None)
        with pytest.raises(SystemExit):
            LOAD(args)
        mock_throwError.assert_called_once_with(17, True, (False, rawPointer))
        mock_throwError.reset_mock()


def test_LoadRegisterPointerUnsupported(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(LoadStore, "throwError")
    mock_throwError.side_effect = mock_exit
    rrs = range(0, 26, 2)
    for rr in rrs:
        args = LineParser(f"LD r0 r{rr}:+", None, None, None)
        with pytest.raises(SystemExit):
            LOAD(args)
        mock_throwError.assert_called_once_with(17, True, (True, f"r{rr}:"))
        mock_throwError.reset_mock()


def test_LoadRegisterPointerOdd(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(LoadStore, "throwError")
    mock_throwError.side_effect = mock_exit
    rrs = range(1, 33, 2)
    for rr in rrs:
        args = LineParser(f"LD r0 r{rr}:", None, None, None)
        with pytest.raises(SystemExit):
            LOAD(args)
        mock_throwError.assert_called_once_with(18, True, ())
        mock_throwError.reset_mock()
