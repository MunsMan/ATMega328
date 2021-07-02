from module.errorHandling.error import throwError
from typing import List


class LineParser:
    def __init__(self, line: str, labelRef, label: str, blockIndex: int) -> None:
        self.lineArr: List[str] = self.splitLine(line)
        self.label = label
        self.blockIndex = blockIndex
        self.rd = self.lineArr[1]
        self.rr = self.lineArr[2] if len(self.lineArr) == 3 else None
        self.opcode, self.cond, self.flag = self._parseOpcode(self.lineArr[0])
        self.__labelRefInstance = labelRef

    @staticmethod
    def _parseOpcode(opcode: str):
        opcode = opcode.upper()
        shortCodes = ['BR', 'CP', 'OR', 'LD']
        longCodes = ['FMULS', 'FMULSU', 'MULSU']
        case = {
            'SHORT': (opcode[0:2], opcode[2:4], ""),
            3: (opcode, "", ""),
            4: (opcode[0:4], opcode[4:6], ""),
            5: (opcode[0:3], opcode[3:5], ""),
            'LONG': LineParser._long(opcode)
        }

        if opcode[0:2] in shortCodes:
            return case["SHORT"]

        if any(map(lambda x: opcode.find(x) != -1, longCodes)):
            return case["LONG"]

        if len(opcode) in case:
            return case[len(opcode)]

        throwError(4, True, opcode)

    @staticmethod
    def _long(opcode: str):
        if len(opcode) >= 7:
            return opcode[:-2], opcode[-2:], ""
        else:
            return opcode, "", ""

    def labelRef(self):
        return self.__labelRefInstance(self.rr if self.rr is not None else self.rd,
                                       self.blockIndex,
                                       self.label)

    def splitLine(self, line: str) -> List[str]:
        if line.find("{") != -1:
            line = line.split("{")
            line = [line[0]] + line[1].split("}")
            line = list(map(str.strip, line))
        else:
            line = line.split(" ")
        return line
