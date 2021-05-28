from typing import List, Tuple
from ..errorHandling import throwError


class FileReader:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.lines: List[Tuple(int, str)] = self._readSourceFile()
        self._cleanFile()

    def _readSourceFile(self):
        try:
            with open(self.filepath) as fd:
                lines = fd.readlines()
        except (OSError, IOError) as e:
            throwError(2, False, (self.filepath, e))
        return zip(range(1, len(lines)+1), lines)

    def _cleanFile(self):
        lines = []
        for index, line in self.lines:
            line = line.replace("\n", "")
            line = line.replace(";", "")
            if line.find("//") != -1:
                line = line[0:line.find("//")]
            line = line.strip()
            if line != "":
                lines.append((index, line))
        self.lines = lines

    def printFile(self):
        for line in self.lines:
            print(line)
