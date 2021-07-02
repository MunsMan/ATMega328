from pytest_mock import MockerFixture

from .. import LoadStore
from ..LoadStore import LOAD
from ..RegisterManager import RegisterManager
from ..instructions import mapInstructions
from ...Parser import LineParser
import random


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
        LoadStore.RegisterManager, "getFreeRegister")
    mock_getFreeRegister.return_value = 16
    rds = range(0, 16)
    rrs = [0, 255] + [random.randint(0, 254) for _ in range(32)]
    for rd in rds:
        for rr in rrs:
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
