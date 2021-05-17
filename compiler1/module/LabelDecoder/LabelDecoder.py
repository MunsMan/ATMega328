from typing import List, Dict, Any


class LabelDecoder:
    def __init__(self, file) -> None:
        self.labels: Dict[str, List[Any]] = {"main": []}
        self.currentLabel: str = "main"
        self.file = file
        self._scanLabels(file)
        self._splitLabels(file)

    def _scanLabels(self, file: List[str]):
        for line in file:
            if self.checkIfLabel(line):
                line = line.replace(":", "")
                self.labels[line] = []

    def getLabels(self):
        return list(self.labels)

    def checkIfLabel(self, line: str) -> bool:
        return line.find(":") != -1

    def getCurrentLabel(self) -> str:
        return self.currentLabel

    def updateCurrentLabel(self, line: str) -> bool:
        if self.checkIfLabel(line):
            self.currentLabel = line.replace(":", "")
            return True
        else:
            return False

    def addInstrutionToLabel(self, instruction) -> None:
        instructions: List[Any] = self.labels.get(self.currentLabel)
        instructions.append(instruction)
        self.labels[self.currentLabel] = instructions

    def _splitLabels(self, file) -> Dict[str, List[str]]:
        for line in file:
            if self.checkIfLabel(line):
                self.updateCurrentLabel(line)
                if self.currentLabel not in self.labels:
                    self.labels[self.currentLabel] = []
            else:
                self.labels[self.currentLabel].append(line)

    def printLabels(self):
        for label in self.labels:
            instructions = self.labels[label]
            print("{label}:".format(label=label))
            for instruction in instructions:
                print("\t{i}".format(i=instruction))

    def labelRef(self):
        pass
