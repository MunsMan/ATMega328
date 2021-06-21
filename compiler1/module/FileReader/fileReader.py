from typing import List, Tuple
from ..errorHandling import throwError
import re


class FileReader:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.lines: List[Tuple[int, str]] = self._readSourceFile()
        self._cleanFile()

    def _readSourceFile(self) -> List[Tuple[int, str]]:
        try:
            with open(self.filepath) as fd:
                lines = fd.readlines()
        except (OSError, IOError) as e:
            throwError(2, False, (self.filepath, e))
        return zip(range(1, len(lines)+1), lines)

    def _cleanFile(self):
        lines = []
        for index, line in self.lines:
            line = re.sub(r'\/\/.*$', "", line)
            line = re.sub(r'[\n|\t|,|;|\s+]', " ", line)
            line = re.sub(r' *- *', "-", line)
            line = re.sub(r' *:', ":", line)
            line = re.sub(r'\s+', " ", line)
            line = line.strip()
            if line != "":
                lines.append((index, line))
        self.lines = lines

    def __str__(self) -> str:
        file = ""
        for lineNum, line in self.lines:
            file += str(lineNum) + "\t" + line + "\n"
        return file
