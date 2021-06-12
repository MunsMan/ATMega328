from module.errorHandling.error import throwError
from typing import List


class LineParser:
    def __init__(self, line: str, labelRef, label: str, blockIndex: int) -> None:
        self.lineArr: List[str] = line.split(" ")
        self.label = label
        self.blockIndex = blockIndex
        self.rd = self.lineArr[1]
        self.rr = self.lineArr[2] if len(self.lineArr) == 3 else None
        self.opcode, self.cond, self.flag = self._parseOpcode(self.lineArr[0])
        self.__labelRefInstance = labelRef

    def _parseOpcode(self, opcode: str):
        case = {
            3: (opcode.upper(), "", ""),
            4: (opcode[0:2].upper(), opcode[2:4].upper(), ""),
            5: (opcode[0:3].upper(), opcode[2:4].upper(), ""),
        }
        if len(opcode) in case:
            return case[len(opcode)]

        throwError(4, True, opcode)

    def labelRef(self):
        return self.__labelRefInstance(self.rr if self.rr is not None else self.rd,
                                       self.blockIndex,
                                       self.label)
