from pytest_mock import MockerFixture
import pytest
from typing import List
from ..fileReader import FileReader


def beforeEach(mocker: MockerFixture, testInput: List[str]):
    mock_readSource = mocker.patch.object(FileReader, "_readSourceFile")
    mock_readSource.return_value = zipLines(testInput)


def zipLines(lines: List[str]):
    return list(zip(range(1, len(lines) + 1), lines))


def test_cleanSemicolon(mocker: MockerFixture):
    rawInput = ["ADD r0 r1;", "BREQ r0;"]
    expected = [(1, "ADD r0 r1"), (2, "BREQ r0")]
    beforeEach(mocker, rawInput)
    fileReader = FileReader("")
    assert(fileReader.lines == expected)


def test_cleanCommas(mocker: MockerFixture):
    rawInput = ["ADD r0, r2,", "BREQ r1, ,"]
    expected = zipLines(["ADD r0 r2", "BREQ r1"])
    beforeEach(mocker, rawInput)
    fileReader = FileReader("")
    assert(fileReader.lines == expected)


def test_cleanComment(mocker: MockerFixture):
    rawInput = ["ADD r0 r1 // Adding Register r1 to r0",
                "BREQ test // jumps to label test if zero flag is set"]
    expected = zipLines(["ADD r0 r1", "BREQ test"])
    beforeEach(mocker, rawInput)
    fileReader = FileReader("")
    assert(fileReader.lines == expected)


def test_removeEmptyLine(mocker: MockerFixture):
    rawInput = ["// I'm just a comment!", "    "]
    expected = []
    beforeEach(mocker, rawInput)
    fileReader = FileReader("")
    assert(fileReader.lines == expected)
