import pytest
from ..LabelDecoder import LabelDecoder


def createRawInput(labelRef):
    return {
        "main": (
            4, [
                (1, lambda: 1),
                (1, lambda: labelRef("loop", 1, "main")),
                (2, lambda: 1),
            ]
        ),
        "hi": (
            5, [
                (1, lambda: 1),
                (1, lambda: 1),
                (1, lambda: 1),
                (1, lambda: 1),
                (1, lambda: labelRef("main", 4, "hi")),
            ]),
        "loop": (
            3, [
                (1, lambda: 1),
                (1, lambda: labelRef("hi", 1, "loop")),
                (1, lambda: labelRef("loop", 2, "loop")),
            ]
        ),
    }


def decodeLabelRef(parsedLabels):
    for label in parsedLabels:
        _, instructions = parsedLabels[label]
        for i, (l, instruction) in enumerate(instructions):
            instructions[i] = (l, instruction())
    return parsedLabels


def test_labelRef():
    labelDecoder = LabelDecoder([])
    rawInput = createRawInput(labelDecoder.labelRef)
    labelDecoder.parsedLabels = rawInput
    res = decodeLabelRef(labelDecoder.parsedLabels)
    assert(res["main"][1][1] == (1, 7))
    assert(res["hi"][1][4] == (1, -9))
    assert(res["loop"][1][1] == (1, -7))
    assert(res["loop"][1][2] == (1, -3))


def test_labelRefAssertion():
    labelDecoder = LabelDecoder([])
    with pytest.raises(AssertionError):
        labelDecoder.labelRef(None, None, None)
