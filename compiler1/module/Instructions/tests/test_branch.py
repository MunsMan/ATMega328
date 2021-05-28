from pytest_mock import MockerFixture
import pytest

from .helper import mock_exit
from ..branch import BRBS
from ..instructions import brbs
from ..helper import twoComplement
from .. import helper
from .. import instructions as Instructions


def test_BRBC_validImmediate(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(Instructions, "throwError")
    flags = range(0, 8)
    offsets = range(-64, 64)
    for flag in flags:
        for offset in offsets:
            numInstructions, instructions = BRBS(flag, offset, None)
            assert(numInstructions == 1)
            assert(instructions() == [brbs(flag, twoComplement(offset, 7))])
    mocker_throwError.assert_not_called()


def test_BRBC_invalidImmediate(mocker: MockerFixture):
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


def test_BRBC_invalidFlag(mocker: MockerFixture):
    mocker_throwError = mocker.patch.object(helper, "throwError")
    mocker_throwError.side_effect = mock_exit
    invalidFlags = [-1, 8]
    validOffset = 1
    for flag in invalidFlags:
        with pytest.raises(SystemExit):
            BRBS(flag, validOffset, None)
        mocker_throwError.assert_called_once_with(
            7, True, (flag, flag.bit_length(), 3))
        mocker_throwError.reset_mock()
