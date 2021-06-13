from module.Parser.LineParser import LineParser
from module.errorHandling.error import throwError
from ..Instructions.commands import LineParser, mapCommmands
from typing import Any, Callable, Dict, List, Tuple
from ..errorHandling import LineRef


Labels = Dict[str, List[Tuple[int, str]]]
Labelname = str
Instruction = Tuple[int, Callable[[], List[int]]]
ParsedLabel = Tuple[int, List[Instruction]]
ParsedLabels = Dict[Labelname, ParsedLabel]


class Parser:
    def __init__(self, labels: Labels, labelRef) -> None:
        self.labelRef = labelRef
        self.currentLabel = "main"
        self.labels: Labels = labels

    def parse(self) -> ParsedLabels:
        for label in self.labels:
            self.labels[label] = self._parseBlock(label, self.labels[label])
        return self.labels

    def _parseBlock(self, labelName: str, labelBlock: List[str]) -> ParsedLabel:
        self.currentLabel = labelName
        instructions = []
        numInstructions = 0
        for blockIndex, (lineNum, line) in enumerate(labelBlock):
            LineRef.setLine(lineNum, line)
            res = mapCommmands(LineParser(
                line, self.labelRef, self.currentLabel, blockIndex))
            numInstructions += res[0]
            instructions.append(res)
        return numInstructions, instructions
