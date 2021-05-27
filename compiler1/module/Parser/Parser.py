from module.Instructions import instructions
from ..Instructions.commands import CommandArgs, mapCommmands
from typing import Any, Callable, Dict, List, Tuple


class Parser:
    def __init__(self, labelRef) -> None:
        self.labelRef = labelRef
        self.label = "main"

    def parseLine(self, line: str, numLine: int) -> Tuple[int, Callable[[], List[int]]]:
        line: List[str] = line.split(" ")
        op, cond, flag = self.parseOpcode(line[0])
        rd = line[1]
        rr = line[2]
        args = CommandArgs(op, rd, rr, cond, flag,
                           self.labelRef, numLine, self.label)
        return mapCommmands(args)

    def parseBlock(self, labelName: str, label: List[str]) -> Tuple[int, List[Tuple[int, Callable[[], List[int]]]]]:
        self.label = labelName
        numLine = 0
        instructions = []
        numInstructions = 0
        for line in label:
            res = self.parseLine(line, numLine)
            numInstructions += res[0]
            instructions.append(res)
            numLine += 1
        return numInstructions, instructions

    def parseLabels(self, labels: Dict[str, List[Any]]):
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
