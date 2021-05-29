from ..Instructions.commands import CommandArgs, mapCommmands
from typing import Any, Callable, Dict, List, Tuple
from ..errorHandling import LineRef


class Parser:
    def __init__(self, labelRef) -> None:
        self.labelRef = labelRef
        self.label = "main"

    def parseLine(self, line: str, numLine: int) -> Tuple[int, Callable[[], List[int]]]:
        line: List[str] = line.split(" ")
        op, cond, flag = self.parseOpcode(line[0])
        rd = line[1]
        rr = line[2] if len(line) == 3 else None
        args = CommandArgs(op, rd, rr, cond, flag,
                           self.labelRef, numLine, self.label)
        return mapCommmands(args)

    def parseBlock(self, labelName: str, label: List[str]) -> Tuple[int, List[Tuple[int, Callable[[], List[int]]]]]:
        self.label = labelName
        instructions = []
        numInstructions = 0
        for blockIndex, (lineNum, line) in enumerate(label):
            LineRef.setLine(lineNum, line)
            res = self.parseLine(line, blockIndex)
            numInstructions += res[0]
            instructions.append(res)
        return numInstructions, instructions

    def parseLabels(self, labels: Dict[str, List[Tuple[int, str]]]):
        for label in labels:
            labels[label] = self.parseBlock(label, labels[label])
        return labels

    def parseOpcode(self, opcode: str):

        case = {
            3: (opcode.upper(), "", ""),
            4: (opcode[0:2].upper(), opcode[2:4].upper(), ""),
            5: (opcode[0:3].upper(), opcode[2:4].upper(), ""),
        }
        if len(opcode) in case:
            return case[len(opcode)]

        print("Error ParseOpcode")
        return "NOP", "", ""
