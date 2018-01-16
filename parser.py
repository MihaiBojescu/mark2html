import tree


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentToken = self.tokens[0]
        self.currentPos = 0
        self.output = ""
        self.tree = tree.Tree()
        self.currentNode = tree.Tree()
        self.currentNode.value = ("root", "root")
        self.iteration = [0]
        self.oldIteration = self.iteration[0]
        self.previousIteration = self.iteration[0]

    def parse(self):
        print("Total number of tokens: {0}".format(len(self.tokens)))
        while(self.previousIteration < len(self.tokens) - 1):
            if(self.definition("table",                [self.tableRow(), self.newline(), self.tableHead(), self.newline(), self.tableRows()])): continue
            if(self.definition("link",                 [self.lbracket(), self.wordListWithSpaces(), self.rbracket(), self.lparanthesis(), self.wordListWithSpaces(), self.rparanthesis()])): continue
            if(self.definition("image",                [self.exclamationMark(), self.lbracket(), self.wordListWithSpaces(), self.rbracket(), self.lparanthesis(), self.wordListWithSpaces(), self.rparanthesis()])): continue
            if(self.definition("heading",              [self.headings(), self.whitespace()])): continue
            if(self.definition("quotation",            [self.rangular(), self.whitespace(), self.wordListWithSpaces(), self.newline()])): continue
            if(self.definition("newlines",             [self.newLines()])): continue
            if(self.definition("italic text",          [self.italic()])): continue
            if(self.definition("bold text",            [self.bold()])): continue
            if(self.definition("bold and italic text", [self.bolditalic()])): continue
            if(self.definition("line break",           [self.linebreak()])): continue
            if(self.definition("code block",           [self.code(), self.code(), self.code(), self.formatedTextBlock(), self.code(), self.code(), self.code()])): continue
            if(self.definition("inline code",          [self.code(), self.formatedTextBlock(), self.code()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.code(), self.code(), self.code(), self.formatedTextBlock(), self.code(), self.code(), self.code()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.code(), self.formatedTextBlock(), self.code()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.wordListWithSpaces()])): continue
            if(self.definition("line break",           [self.line(), self.line(), self.line(), self.newline()])): continue
            if(self.definition("line break",           [self.star(), self.star(), self.star(), self.newline()])): continue
            if(self.definition("line break",           [self.underscore(), self.underscore(), self.underscore(), self.newline()])): continue
            if(self.definition("words",                [self.wordListWithSpaces()])): continue

            if(self.previousIteration == self.oldIteration):
                print("Stuck at token number: {0}, token: {1}".format(self.oldIteration, self.tokens[self.oldIteration]))
                break
            self.oldIteration = self.previousIteration

    def getOutput(self):
        return self.output

    def definition(self, type, definitionList):
        if(self.definitionRecursive(definitionList, 0)):
            print("Type: {0}, list: ".format(type), end='')
            print(self.iteration)
            self.previousIteration = self.iteration[0]
            self.iteration = [self.previousIteration]
            return True
        else:
            self.iteration = [self.previousIteration]
            return False

    def definitionRecursive(self, definitionList, i):
        if i > len(definitionList) - 1:
            return True
        elif definitionList[i]:
            return self.definitionRecursive(definitionList, i + 1)
        else:
            return False

    def printoutput(self, node):
        for element in node.nodeList:
            print(element.value)
            self.printoutput(element)

    def heading1(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading1":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def heading2(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading2":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def heading3(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading3":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def heading4(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading4":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def heading5(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading5":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def heading6(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "heading6":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def multispace(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "whitespace":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def singlespace(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "singlespace":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def tab(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "tab":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def newline(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "newline":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def star(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "*":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def tilde(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "~":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False


    def verticalLine(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "|":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def line(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "-":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def code(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "`":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def underscore(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "_":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def exclamationMark(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "!":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def lbracket(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "[":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def rbracket(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "]":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def lparanthesis(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "(":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def rparanthesis(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == ")":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def lbrace(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "{":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def rbrace(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "}":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def langular(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "<":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def rangular(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == ">":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def linebreak(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "linebreak":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def startBoldHTML(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "sbold":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def endBoldHTML(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "ebold":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def startItalicHTML(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "sitalic":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def endItalicHTML(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "eitalic":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def word(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "word":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def symbol(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "symbols":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def headings(self):
        return self.heading1() or self.heading2() or self.heading3() or self.heading4() or self.heading5() or self.heading6()

    def whitespace(self):
        found = False
        while self.multispace() or self.singlespace() or self.tab():
            found = True
        return found

    def wordListWithSpaces(self):
        found = False
        while self.word() or self.whitespace() or self.symbol() or self.line() or self.tilde() or self.exclamationMark():
            found = True
        return found

    def formatedTextBlock(self):
        found = False
        while self.word() or self.whitespace() or self.symbol() or self.line() or self.tilde() or self.newLines() or self.lbrace() or self.rbrace() \
        or self.lparanthesis() or self.rparanthesis() or self.langular() or self.rangular() or self.lbracket() or self.rbracket() or self.startBoldHTML() \
        or self.endBoldHTML() or self.startItalicHTML() or self.endItalicHTML() or self.headings() or self.star() or self.tilde() or self.underscore() \
        or self.verticalLine() or self.exclamationMark():
            found = True
        return found

    def italic(self):
        if self.star() and self.wordListWithSpaces() and self.star():
            return True
        elif self.startItalicHTML() and self.wordListWithSpaces() and self.endItalicHTML():
            return True
        else:
            return False

    def bold(self):
        if self.star() and self.star() and self.wordListWithSpaces() and self.star() and self.star():
            return True
        elif self.startBoldHTML() and self.wordListWithSpaces() and self.endBoldHTML():
            return True
        else:
            return False

    def bolditalic(self):
        if self.star() and self.star() and self.star() and self.wordListWithSpaces() and self.star() and self.star() and self.star():
            return True
        elif self.startBoldHTML() and self.startItalicHTML() and self.wordListWithSpaces and self.endItalicHTML() and self.startBoldHTML():
            return True
        elif self.startItalicHTML() and self.startBoldHTML() and self.wordListWithSpaces and self.endBoldHTML() and self.startItalicHTML():
            return True
        return False

    def newLines(self):
        found = False
        while self.newline():
            found = True
        return found

    def lines(self):
        found = False
        while self.line():
            found = True
        return found

    def tableRow(self):
        if self.wordListWithSpaces():
            found = False
            while self.verticalLine() or self.wordListWithSpaces():
                found = True
            if self.iteration[len(self.iteration) - 1][1] != "|":
                return found
            else:
                return False
        else:
            return False

    def tableHead(self):
        if self.lines():
            found = False
            while self.verticalLine() or self.lines() or self.whitespace():
                found = True
            if self.iteration[len(self.iteration) - 1][1] != "|":
                return found
            else:
                return False
        else:
            return False

    def tableRows(self):
        found = False
        while self.tableRow():
            found = True
        return found
