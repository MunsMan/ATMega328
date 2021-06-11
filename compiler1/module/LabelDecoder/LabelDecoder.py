from typing import Callable, List, Dict, Any, Tuple

ParsedFileType = Dict[str, Tuple[int,
                                 List[Tuple[int, Callable[[], List[int]]]]]]
LabelType = Dict[str, List[Any]]


class LabelDecoder:
    def __init__(self, file) -> None:
        self.labels: LabelType = {"main": []}
        self.currentLabel: str = "main"
        self.file = file
        self._parse()
        self.parsedLabels: ParsedFileType = {}

    def _parse(self):
        self._scanLabels()
        self._splitLabels()

    def _scanLabels(self):
        for _, line in self.file:
            if self._checkIfLabel(line):
                label = line[:-1]
                self.labels[label] = []

    def _checkIfLabel(self, line: str) -> bool:
        return line[-1] == ":"

    def _updateCurrentLabel(self, line: str) -> bool:
        if self._checkIfLabel(line):
            self.currentLabel = line[:-1]
            return True
        else:
            return False

    def addInstrutionToLabel(self, instruction) -> None:
        instructions: List[Any] = self.labels.get(self.currentLabel)
        instructions.append(instruction)
        self.labels[self.currentLabel] = instructions

    def _splitLabels(self) -> Dict[str, List[str]]:
        for lineNum, line in self.file:
            if self._checkIfLabel(line):
                self._updateCurrentLabel(line)
                if self.currentLabel not in self.labels:
                    self.labels[self.currentLabel] = []
            else:
                self.labels[self.currentLabel].append((lineNum, line))

    def printLabels(self):
        for label in self.labels:
            instructions = self.labels[label]
            print("{label}:".format(label=label))
            for instruction in instructions:
                print("\t{i}".format(i=instruction))

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
            offsetLabels = labels[currentLabelIndex+1:jumpLabelIndex]
            offset += sum(map(lambda x: self.parsedLabels[x][0], offsetLabels))
            if len(currentLabel) != blockIndex:
                currentLabelInstructions = currentLabelInstructions[blockIndex+1:]
                offset += sum(map(lambda x: x[0], currentLabelInstructions))
        else:
            offsetLabels = labels[jumpLabelIndex: currentLabelIndex]
            offset -= sum(map(lambda x: self.parsedLabels[x][0], offsetLabels))
            offset -= sum(map(lambda x: x[0],
                          currentLabelInstructions[:blockIndex]))
            offset -= 1
        return int(offset)

    def decodeLabelRef(self):
        assert len(self.parsedLabels) != 0
        for label in self.parsedLabels:
            _, instructions = self.parsedLabels[label]
            for i, (l, instruction) in enumerate(instructions):
                instructions[i] = (l, instruction())
        return self.parsedLabels
