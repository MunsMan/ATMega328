#!/usr/bin/python3

from typing import List
import sys
from module import FileReader, throwError, LabelDecoder


def main():
    if len(sys.argv) < 2:
        throwError(1, False)
    filepath = sys.argv[1]
    fileReader = FileReader(filepath)
    labelDecoder = LabelDecoder(fileReader.lines)
    labelDecoder.printLabels()


if __name__ == "__main__":
    main()
