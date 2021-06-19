#!/usr/bin/python3
import sys
from module import FileReader, throwError, LabelDecoder, Parser, Output


def main():
    if len(sys.argv) < 2:
        throwError(1, False)
    filepath = sys.argv[1]
    fileReader = FileReader(filepath)
    labelDecoder = LabelDecoder(fileReader.lines)
    parsedLabels = Parser(labelDecoder.labels, labelDecoder.labelRef).parse()
    labelDecoder.parsedLabels = parsedLabels
    output = []
    for label in parsedLabels:
        print(label)
        _, instructions = parsedLabels[label]
        for _, instruction in instructions:
            for inst in instruction():
                print("\t0x%04X" % inst)
                output.append(inst)
    out = Output(output)
    out.bin()
    out.hex()


if __name__ == "__main__":
    main()
