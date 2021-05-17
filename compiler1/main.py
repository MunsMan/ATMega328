from typing import List
import sys
from module import FileReader, throwError, LabelDecoder


def main():
    if len(sys.argv) < 2:
        throwError(1, False)
    filepath = sys.argv[1]
    fileReader = FileReader(filepath)
    fileReader.printFile()
    labelDecoder = LabelDecoder()
    labelDecoder.scanLabels(fileReader.lines)
    print(labelDecoder.getLabels())
    print(labelDecoder.splitLabels(fileReader.lines))


if __name__ == "__main__":
    main()
