from compiler1.module.Instructions.commands import mapCommmands
from typing import Callable, List, Tuple


class Parser:
    def __init__(self, labelRef) -> None:
        self.labelRef = labelRef

    def parseLine(self, line: str):
        line: List[str] = line.split(" ")
        op, cond, flag = self.parseOpcode(line[0])
        rd = line[1]
        rr = line[2]
        mapCommmands(op, cond, flag, rd, rd, self.labelRef)

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
