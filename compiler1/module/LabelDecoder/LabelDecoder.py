from typing import Callable, List, Dict, Any, Tuple


class LabelDecoder:
    def __init__(self, file) -> None:
        self.labels: Dict[str, List[Any]] = {"main": []}
        self.currentLabel: str = "main"
        self.file = file
        self._scanLabels(file)
        self._splitLabels(file)
        self.parsedLabels: Dict[str, Tuple[int, List[Tuple[int, Callable[[], List[int]]]]]] = {}

    def _scanLabels(self, file: List[str]):
        for line in file:
            if self.checkIfLabel(line):
                line = line.replace(":", "")
                self.labels[line] = []

    def getLabels(self):
        return self.labels

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

    def setParsedLabels(self, parsedLabels):
        self.parsedLabels = parsedLabels


    def labelRef(self, jumpLabel: str, blockIndex: int, currentLabel: str) -> int:
        """[summary]

        Args:
            label (str): jump to label
            blockIndex (int): index in current label block
            currentLabel (str): label of the labelRef call

        Returns:
            int: signed jump offset 
        """
        assert len(self.parsedLabels) != 0
        _, currentLabelInstructions = self.parsedLabels[currentLabel]
        offset = 0
        
        labels = list(self.parsedLabels.keys())
        currentLabelIndex = labels.index(currentLabel)
        jumpLabelIndex = labels.index(jumpLabel)

        if currentLabelIndex < jumpLabelIndex:
            labels = labels[currentLabelIndex+1:jumpLabelIndex]
            offset += sum(map(lambda x: self.parsedLabels[x][0], labels))
            if len(currentLabel) != blockIndex:
                currentLabelInstructions = currentLabelInstructions[blockIndex+1:]
                offset += sum(map(lambda x: x[0], currentLabelInstructions))
        else:
            labels = labels[jumpLabelIndex: currentLabelIndex]
            offset -= sum(map(lambda x: self.parsedLabels[x][0], labels))
            offset -= sum(map(lambda x: x[0], currentLabelInstructions[:blockIndex]))
        return int(offset)
        


