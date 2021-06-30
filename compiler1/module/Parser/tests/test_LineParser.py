from module.Parser.LineParser import LineParser


def test_parseOpcode():
    inputs = ["BREQ", "ADD"]
    expecteds = [("BR", "EQ", ""), ("ADD", "", "")]
    for i in range(len(inputs)):
        assert expecteds[i] == LineParser._parseOpcode(inputs[i])
