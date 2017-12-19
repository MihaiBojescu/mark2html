#!/usr/bin/env python3
import os
import sys


def handleArgs(args):
    IO = [None, None]
    if len(args) == 1:
        print("Usage:")
        print("markdown2html <markdown document> [<output file>]")
        print("\nIt will use output.css or <output file>.css file for "
              "styling. The file is located inside the css folder.")
        sys.exit(1)
    elif len(args) >= 2:
        if os.path.exists(args[1]):
            if os.path.splitext(args[1])[1] == ".md":
                IO[0] = args[1]
            else:
                print("Input file isn't a markdown document.")
                sys.exit(1)
        else:
            print("Input file not valid.")
            sys.exit(1)

        if len(args) == 3:
            if os.path.exists(args[2]):
                IO[1] = args[2]
            else:
                print("Input file path not valid.")
                sys.exit(1)

        return IO


def readFile(filename):
    buffer = ""
    try:
        file = os.open(filename, os.O_RDONLY)
        buffer = os.read(file, os.stat(filename).st_size)
        os.close(file)
    except (IOError, OSError):
        print("Reading input file error.")
        sys.exit(2)
    return buffer.decode()


def headingHandler(buffer, line):
    output = ""

    for i in range(0, len(line)):
        if not line[i] == '#':
            break

    line = line.replace("#", "")
    line = line.strip()
    header = ''.join(("<h", str(i), ">"))
    closingHeader = ''.join(("</h", str(i), ">"))
    output = ''.join((buffer, header, line, closingHeader, '\n'))

    return output


def horizontalBreakHandler(buffer):
    output = ''.join((buffer, "<hr>\n"))
    return output


def codeBlockHandler(buffer, lines, currentIndex):
    output = ""
    newIndex = currentIndex
    found = False

    for newIndex in range(currentIndex + 1, len(lines)):
        if lines[newIndex] == "```":
            found = True
            break

    if found:
        codeBlock = '\n'.join(lines[currentIndex + 1:newIndex])
        output = ''.join((buffer, "<pre>\n", codeBlock, "\n</pre>\n"))
        return (output, newIndex + 1)

    else:
        output = ''.join((buffer, lines[currentIndex]))
        return (output, currentIndex + 1)


def codeHandler(buffer, remainingLines):
    output = ''.join((buffer))
    return output


def breakHandler(buffer, line):
    output = ''.join((buffer, line.replace("<br>", "\n")))
    return output


def handleBuffer(buffer):
    outputBuffer = str("<!DOCTYPE html>\n"
                       "<html>\n"
                       "    <head>\n"
                       "        <link rel=\"stylesheet\" type=\"text/css\" href=\"css/output.css\"\n"
                       "    </head>\n"
                       "    <body>\n")

    lines = buffer.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        line = line.strip()

        if line.startswith("#"):
            outputBuffer = headingHandler(outputBuffer, line)

        elif line == "---" or line == "___" or line == "***":
            outputBuffer = horizontalBreakHandler(outputBuffer)

        elif line.startswith("```"):
            (outputBuffer, newIndex) = codeBlockHandler(outputBuffer,
                                                        lines,
                                                        i)
            i = newIndex

        # elif line.find('`'):
        #     outputBuffer = codeHandler(outputBuffer, lines[i:])
        #
        elif line.find('<br>'):
            outputBuffer = breakHandler(outputBuffer, line)

        else:
            outputBuffer = ''.join((outputBuffer, line, "\n"))

        i += 1

    return '\n'.join((outputBuffer,
                      "    </body>",
                      "</html>"))


def writeFile(filename, buffer):
    if filename is None:
        filename = "output.html"

    try:
        file = os.open(filename, os.O_WRONLY | os.O_CREAT)
        os.write(file, buffer.encode())
        os.close(file)
    except (IOError, OSError):
        print("Writing output file error.")
        sys.exit(2)

    folder = os.path.abspath(os.path.join(filename, os.pardir))
    cssfolder = ''.join((folder, "/css/"))
    cssfile = ''.join((cssfolder, os.path.splitext(filename)[0], ".css"))

    if not os.path.exists(cssfolder) or not os.path.isdir(cssfolder):
        try:
            os.mkdir(cssfolder)
            print("Created css folder.")
        except OSError:
            print("Can't create css folder.")
            sys.exit(2)
    if not os.path.exists(cssfile):
        try:
            file = os.open(cssfile, os.O_CREAT)
            os.close(file)
            print("Created css file")
        except OSError:
            print("Can't create css file.")
            sys.exit(2)


def main(args):
    IO = handleArgs(args)
    buffer = readFile(IO[0])
    outputBuffer = handleBuffer(buffer)
    writeFile(IO[1], outputBuffer)


if __name__ == '__main__':
    main(sys.argv)