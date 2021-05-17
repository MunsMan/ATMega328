from typing import Callable, List, Tuple


class Parser:
    def __init__(self) -> None:
        pass

    def parseLine(self, line: str):
        line: List[str] = line.split(" ")
        op, cond, flag = self.parseOpcode(line[0])

    def parseOpcode(self, opcode: str):
        if len(opcode) == 3:
            return opcode.upper(), "", ""
        else:
            # ToDo: implement parse Condition and Flag
            print("Error ParseOpcode")
            return "NOP", "", ""
