#!/usr/bin/env python3
#
# TODO: implement parser
#
import sys
import os
from tokenizer import Tokenizer
from parser import Parser

defaultCss = """h1, h2, h3, h4, h5, h6, html, a
{
    font-family: sans-serif;
}

img
{
    /* margin-left: 37.5%; */
    margin-bottom: 4em;
    width: 25%;
}

body
{
    padding: 5em 25% 5em 25%;
}

h1
{
    font-size: 3em;
}

h2
{
    font-size: 2.5em;
}

h3
{
    font-size: 2em;
}

ul
{
    margin: 0em;
}

blockquote
{
    margin: 0px;
    padding: 1em;
    border-left: 0.5em solid #ccc;
    background: #eee;
}

hr
{
    color: fff;
    border: 0px 0px 1px 0px;
}

video
{
    width: 100%;
}

audio
{
    width: 100%;
}

code
{
    font-size: 1.4em;
    background: #eee;
}

pre
{
    background: #eee;
    padding: 1em 0px 1em 0px;
}
                """

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
        with open(filename, 'w+') as file:
            file.write(buffer)
        if not os.path.exists("output.css"):
            with open("output.css", "w+") as css:
                css.write(defaultCss)
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
        # print(outputBuffer)

        if(len(sys.argv) == 3):
            writeFile(sys.argv[2], outputBuffer)
        else:
            writeFile("output.html", outputBuffer)


if __name__ == '__main__':
    main()
