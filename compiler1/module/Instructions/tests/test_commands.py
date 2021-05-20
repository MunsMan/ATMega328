from ..instructions import add
import pytest
from pytest_mock import MockerFixture
from ..commands import ADD, CommandArgs
from .. import commands


def test_addTwoRegister(mocker: MockerFixture):
    mock_throwError = mocker.patch.object(commands, "throwError")
    rds = range(0, 32)
    rrs = range(0, 32)
    args = CommandArgs("ADD", "", "", 0, 0, None, None, "")

    for rd in rds:
        for rr in rrs:
            if rd == rr:
                continue
            args.rr = 'r' + str(rr)
            args.rd = 'r' + str(rd)
            numInstructions, instructions = ADD(args)
            assert numInstructions == 1
            assert instructions() == [add(rd, rr)]
    mock_throwError.assert_not_called()
