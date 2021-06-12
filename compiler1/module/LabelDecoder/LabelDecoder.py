from typing import Callable, List, Dict, Any, Tuple

ParsedFileType = Dict[str, Tuple[int,
                                 List[Tuple[int, Callable[[], List[int]]]]]]
LabelType = Dict[str, List[Any]]


class LabelDecoder:
    def __init__(self, file) -> None:
        self.file = file
        self.labels: LabelType = {"main": []}
        self.parsedLabels: ParsedFileType = {}
        self.currentLabel: str = "main"
        self._splitLabels()

    def _splitLabels(self) -> Dict[str, List[str]]:
        for lineNum, line in self.file:
            if line[-1] == ":":
                self.currentLabel = line[:-1]
                if self.currentLabel not in self.labels:
                    self.labels[self.currentLabel] = []
            else:
                self.labels[self.currentLabel].append((lineNum, line))

    def printLabels(self):
        for label in self.labels:
            instructions = self.labels[label]
            print(f"{label}:")
            [print(f"\t{instruction}") for instruction in instructions]

    def labelRef(self, jumpLabel: str, labelBlockIndex: int, currentLabel: str) -> int:
        assert len(self.parsedLabels) != 0
        _, currentLabelInstructions = self.parsedLabels[currentLabel]
        offset = 0

        labels = list(self.parsedLabels.keys())
        currentLabelIndex = labels.index(currentLabel)
        jumpLabelIndex = labels.index(jumpLabel)

        if currentLabelIndex < jumpLabelIndex:
            offsetLabels = labels[currentLabelIndex+1:jumpLabelIndex]
            offset += sum(map(lambda x: self.parsedLabels[x][0], offsetLabels))
            if len(currentLabel) != labelBlockIndex:
                currentLabelInstructions = currentLabelInstructions[labelBlockIndex+1:]
                offset += sum(map(lambda x: x[0], currentLabelInstructions))
        else:
            offsetLabels = labels[jumpLabelIndex: currentLabelIndex]
            offset -= sum(map(lambda x: self.parsedLabels[x][0], offsetLabels))
            offset -= sum(map(lambda x: x[0],
                          currentLabelInstructions[:labelBlockIndex]))
            offset -= 1
        return int(offset)
