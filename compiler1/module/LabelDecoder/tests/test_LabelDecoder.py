from unittest.mock import Mock
from ..LabelDecoder import LabelDecoder
from typing import List
from pytest_mock import MockerFixture


def zipLines(lines: List[str]):
    return list(zip(range(1, len(lines)+1), lines))


def test_scanLabels(mocker: MockerFixture):
    mocker.patch.object(LabelDecoder, "_parse")
    rawInput = zipLines(["label1:", "ADD r1 r2", "test:",
                         "BREQ r1", "loop:", "MOV r1 #5"])
    expected = {"label1": [], "test": [], "loop": [], "main": []}
    labelDecoder = LabelDecoder(rawInput)
    labelDecoder._scanLabels()

    assert(labelDecoder.labels == expected)


def test_splitLabels():
    rawInput = zipLines(["MOV r4 r3", "label1:", "ADD r1 r2", "test:",
                         "BREQ r1", "loop:", "MOV r1 #5", "MOV r1 #5"])
    expected = {
        "label1": [(3, "ADD r1 r2")],
        "test": [(5, "BREQ r1")],
        "loop": [(7, "MOV r1 #5"), (8, "MOV r1 #5")],
        "main": [(1, "MOV r4 r3")]}
    labelDecoder = LabelDecoder(rawInput)
    assert(labelDecoder.labels == expected)
