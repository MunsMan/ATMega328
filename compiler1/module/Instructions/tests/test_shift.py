from ..instructions import mapInstructions
from ..Shift import shift
from ...Parser import LineParser


def test_shift():
    rds = range(0, 32)
    rrs = range(0, 8)
    opcodes = ["ASR", "LSL", "LSR"]
    for rd in rds:
        for rr in rrs:
            for opcode in opcodes:
                num = rr if rr != 0 else ""
                args = LineParser(
                    f"{opcode} r{rd} {num}".strip(), None, None, None)
                numInstructions, instructions = shift(args)
                numExpected = rr if rr != 0 else 1
                expected = [mapInstructions(opcode.lower())(rd)] * numExpected
                assert numExpected == numInstructions
                assert expected == instructions()
