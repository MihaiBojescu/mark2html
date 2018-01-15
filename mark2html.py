#!/usr/bin/env python3
#
# TODO: implement parser
#
import sys
from tokenizer import Tokenizer
from parser import Parser


def readFile(filename):
    try:
        with open(filename, 'r') as file:
            buffer = file.read()
            return buffer
    except OSError as e:
        print(e)
        sys.exit(1)


def writeFile(filename, buffer):
    try:
        with open(filename, 'r') as file:
            file.write(buffer)
    except OSError as e:
        print(e)
        sys.exit(1)


def main():
    inputBuffer = ""
    outputBuffer = ""

    if(len(sys.argv) >= 2):
        inputBuffer = readFile(sys.argv[1])

        tokenizer = Tokenizer(inputBuffer)
        tokenizer.tokenize()
        tokens = tokenizer.getTokens()

        parser = Parser(tokens)
        parser.parse()
        outputBuffer = parser.getOutput()

        if(len(sys.argv) == 3):
            writeFile(sys.argv[2], outputBuffer)
        else:
            writeFile("output.html", outputBuffer)


if __name__ == '__main__':
    main()
