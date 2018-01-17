import tree


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentId = 0
        self.output = ""
        self.tree = tree.Tree()
        self.tree.value = "<html><head><link href=\"output.css\" rel=\"stylesheet\" type=\"text/css\"></head>"
        self.iteration = [0]
        self.oldIteration = self.iteration[0]
        self.previousIteration = self.iteration[0]
        self.insideCode = False
        self.insideBold = False
        self.insideItalic = False
        self.insideItalicBold = False
        self.insideStrikethrough = False
        self.insideQuotation = False
        self.ids = []

    def parse(self):
        # print("Total number of tokens: {0}".format(len(self.tokens)))
        while(self.previousIteration < len(self.tokens) - 1):
            if(self.definition("reference",            [self.reference(), self.newline()])): continue
            if(self.definition("top",                  [self.top(), self.newline()])): continue
            if(self.definition("table",                [self.tableRow(), self.newline(), self.tableHead(), self.newline(), self.tableRows()])): continue
            if(self.definition("table",                [self.tableRow(), self.newline(), self.tableHead()])): continue
            if(self.definition("link",                 [self.lbracket(), self.wordListWithSpaces(), self.rbracket(), self.lparanthesis(), self.wordListWithSpaces(), self.rparanthesis()])): continue
            if(self.definition("media",                [self.exclamationMark(), self.lbracket(), self.wordListWithSpaces(), self.rbracket(), self.lparanthesis(), self.wordListWithSpaces(), self.rparanthesis()])): continue
            if(self.definition("heading",              [self.headings(), self.whitespace(), self.formattedWordList()])): continue
            if(self.definition("quotation",            [self.rangular(), self.whitespace(), self.formattedWordList(), self.newline()])): continue
            if(self.definition("newlines",             [self.newLines()])): continue
            if(self.definition("strikethrough",        [self.strikethrough()])): continue
            if(self.definition("italic text",          [self.italic()])): continue
            if(self.definition("bold text",            [self.bold()])): continue
            if(self.definition("bold and italic text", [self.bolditalic()])): continue
            if(self.definition("line break",           [self.linebreak()])): continue
            if(self.definition("code block",           [self.codeBlock()])): continue
            if(self.definition("inline code",          [self.inlineCode()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.formattedWordList()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.codeBlock()])): continue
            if(self.definition("unordered list",       [self.star(), self.whitespace(), self.inlineCode()])): continue
            if(self.definition("line break",           [self.line(), self.line(), self.line(), self.newline()])): continue
            if(self.definition("line break",           [self.star(), self.star(), self.star(), self.newline()])): continue
            if(self.definition("line break",           [self.underscore(), self.underscore(), self.underscore(), self.newline()])): continue
            if(self.definition("words",                [self.wordListWithSpaces()])): continue

            if(self.previousIteration == self.oldIteration):
                print("Stuck at token number: {0}, token: {1}".format(self.oldIteration, self.tokens[self.oldIteration]))
                break
            self.oldIteration = self.previousIteration

    def getOutput(self):
        # self.printOutput(self.tree)
        self.buildOutput(self.tree)
        self.generateReference()
        return self.output

    def printOutput(self, node):
        for element in node.nodeList:
            print(element.value)
            self.printoutput(element)

    def buildOutput(self, node):
        if node.value == "<h1>":
            self.output += node.value[:3] + " id=\"heading" + str(self.currentId) + "\"" + node.value[3:]
            self.currentId += 1
        elif node.value == "<toptag>":
            self.output += "<a href=\"#\">Go back to top</a>"
        else:
            self.output += node.value
        for element in node.nodeList:
            self.buildOutput(element)
        if node.value[0] == "<" and node.value != "<br>":
            self.output += node.value[:1] + "/" + node.value[1:]

    def generateReference(self):
        self.generateReferenceRecursive()
        output = "<h1>Reference</h1>\n"
        for item in self.ids:
            output += "<a href=\"" + item[0] + "\">" + item[1] + "</a><br>"
        self.output = self.output.replace("<referencetag>\n</referencetag>", output);

    def generateReferenceRecursive(self):
        pos = 0
        pos = self.output.find("<h1 id=\"")
        while pos != -1:
            self.ids.append(("#" + self.output[pos + 8: self.output.find("\"", pos + 8)], self.output[self.output.find(">", pos + 8) + 1: self.output.find("</h1>", pos + 9)]))
            pos = self.output.find("<h1 id=\"", pos + 1)


    def definition(self, type, definitionList):
        if(self.definitionRecursive(definitionList, 0)):
            # print("Type: {0}, list: ".format(type), end='')
            # print(self.iteration)
            if type != "newlines":
                newNode = tree.Tree()
                self.tree.nodeList.append(newNode)
                self.buildTree(self.iteration[1:], newNode)
            else:
                newNode = tree.Tree()
                newNode.value = "<br>"
                self.tree.nodeList.append(newNode)
            self.previousIteration = self.iteration[0]
            self.iteration = [self.previousIteration]
            return True
        else:
            self.iteration = [self.previousIteration]
            return False
        # print("\n\n")

    def definitionRecursive(self, definitionList, i):
        if i > len(definitionList) - 1:
            return True
        elif definitionList[i]:
            return self.definitionRecursive(definitionList, i + 1)
        else:
            return False

    def buildTree(self, iteration, currentElement):
        if len(iteration) != 0:
            if iteration[0][1] == "reference":
                newNode = tree.Tree()
                currentElement.value = "<referencetag>"
                self.createReference = True
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "top":
                newNode = tree.Tree()
                currentElement.value = "<toptag>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading1":
                newNode = tree.Tree()
                currentElement.value = "<h1>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading2":
                newNode = tree.Tree()
                currentElement.value = "<h2>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading3":
                newNode = tree.Tree()
                currentElement.value = "<h3>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading4":
                newNode = tree.Tree()
                currentElement.value = "<h4>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading5":
                newNode = tree.Tree()
                currentElement.value = "<h5>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "heading6":
                newNode = tree.Tree()
                currentElement.value = "<h6>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif len(iteration) >= 4 and iteration[0][1] == "-" and iteration[1][1] == "-" and iteration[2][1] == "-" and iteration[3][1] == "newline":
                    newNode = tree.Tree()
                    currentElement.value = "<hr>"
                    self.buildTree(iteration[4:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)

            elif len(iteration) >= 4 and iteration[0][1] == "*" and iteration[1][1] == "*" and iteration[2][1] == "*" and iteration[3][1] == "newline":
                    newNode = tree.Tree()
                    currentElement.value = "<hr>"
                    self.buildTree(iteration[4:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)

            elif len(iteration) >= 4 and iteration[0][1] == "_" and iteration[1][1] == "_" and iteration[2][1] == "_" and iteration[3][1] == "newline":
                    newNode = tree.Tree()
                    currentElement.value = "<hr>"
                    self.buildTree(iteration[4:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)

            elif len(iteration) >= 3 and iteration[0][1] == "`" and iteration[1][1] == "`" and iteration[2][1] == "`":
                if not self.insideCode:
                    newNode = tree.Tree()
                    newNode.value = "<pre>"
                    currentElement.value = "<code>"
                    newNode2 = tree.Tree()
                    self.insideCode = True
                    self.buildTree(iteration[3:], newNode2)
                    if newNode2.value is not None:
                        currentElement.nodeList.append(newNode)
                        newNode.nodeList.append(newNode2)
                    self.insideCode = False

            elif iteration[0][1] == "`":
                if not self.insideCode:
                    newNode = tree.Tree()
                    currentElement.value = "<code>"
                    self.insideCode = True
                    self.buildTree(iteration[1:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideCode = False

            elif len(iteration) >= 2 and iteration[0][1] == ">" and iteration[1][1] in ("singlespace", "multispace", "tab"):
                if not self.insideQuotation:
                    newNode = tree.Tree()
                    currentElement.value = "<blockquote>"
                    self.buildTree(iteration[2:], newNode)
                    self.insideQuotation = True
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideQuotation = False
                else:
                    self.buildTree(iteration[2:], currentElement)

            elif iteration[0][1] == "linebreak":
                newNode = tree.Tree()
                currentElement.value = "<br>"
                self.buildTree(iteration[1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif len(iteration) >= 3 and iteration[0][1] == "*" and iteration[1][1] == "*" and iteration[2][1] == "*":
                if not self.insideItalicBold:
                    newNode2 = tree.Tree()
                    newNode = tree.Tree()
                    newNode.value = "<i>"
                    currentElement.value = "<b>"
                    self.insideItalicBold = True
                    self.buildTree(iteration[3:], newNode2)
                    if newNode2.value is not None:
                        newNode.nodeList.append(newNode2)
                        currentElement.nodeList.append(newNode)
                    self.insideItalicBold = False

            elif len(iteration) >= 2 and iteration[0][1] == "*" and iteration[1][1] == "*":
                if not self.insideBold:
                    newNode = tree.Tree()
                    currentElement.value = "<b>"
                    self.insideBold = True
                    self.buildTree(iteration[2:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideBold = False

            elif len(iteration) >= 2 and iteration[0][1] == "*" and iteration[1][1] in ("singlespace", "multispace", "tab"):
                if not self.insideItalic:
                    newNode2 = tree.Tree()
                    newNode = tree.Tree()
                    newNode.value = "<li>"
                    currentElement.value = "<ul>"
                    self.insideItalic = True
                    self.buildTree(iteration[2:], newNode2)
                    if newNode2.value is not None:
                        newNode.nodeList.append(newNode2)
                        currentElement.nodeList.append(newNode)
                    self.insideItalic = False

            elif iteration[0][1] == "*":
                if not self.insideItalic:
                    newNode = tree.Tree()
                    currentElement.value = "<i>"
                    self.insideItalic = True
                    self.buildTree(iteration[1:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideItalic = False

            elif iteration[0][1] == "sbold":
                if not self.insideItalic:
                    newNode = tree.Tree()
                    currentElement.value = "<b>"
                    self.insideBold = True
                    self.buildTree(iteration[1:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideBold = False

            elif iteration[0][1] == "sitalic":
                if not self.insideItalic:
                    newNode = tree.Tree()
                    currentElement.value = "<i>"
                    self.insideItalic = True
                    self.buildTree(iteration[1:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideItalic = False

            elif len(iteration) >= 2 and iteration[0][1] == "~" and iteration[1][1] == "~":
                if not self.insideStrikethrough:
                    newNode = tree.Tree()
                    currentElement.value = "<strike>"
                    self.insideStrikethrough = True
                    self.buildTree(iteration[2:], newNode)
                    if newNode.value is not None:
                        currentElement.nodeList.append(newNode)
                    self.insideStrikethrough = False

            elif len(iteration) >= 2 and iteration[0][1] == "!" and iteration[1][1] == "["  and not self.insideCode:
                i = 0
                while i < len(iteration):
                    if iteration[i][1] == "(":
                        break
                    else:
                        i += 1

                newNode = tree.Tree()
                alttext = ""
                link = ""
                for j in range(2, i - 1):
                    alttext += iteration[j][0]

                for j in range(i + 1, len(iteration)):
                    if(iteration[j][1] == ")"):
                        break
                    else:
                        link += iteration[j][0]

                if link.rsplit(".")[1] == "mp4":
                    currentElement.value = "<video src=\"" + link + "\" alttext=\"" + alttext + "\" controls>"
                elif link.rsplit(".")[1] == "ogg":
                    currentElement.value = "<audio src=\"" + link + "\" alttext=\"" + alttext + "\" controls>"
                else:
                    currentElement.value = "<img src=\"" + link + "\" alttext=\"" + alttext + "\">"
                while i < len(iteration):
                    if iteration[i][1] == ")":
                        break
                    else:
                        i += 1
                self.buildTree(iteration[i + 1:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)

            elif iteration[0][1] == "[" and not self.insideCode:
                i = 0
                while i < len(iteration):
                    if iteration[i][1] == "]":
                        break
                    else:
                        i += 1
                if i != len(iteration):
                    text = ""
                    link = ""
                    for j in range(1, i):
                        text += iteration[j][0]

                    for j in range(i + 2, len(iteration)):
                        if(iteration[j][1] == ")"):
                            break
                        else:
                            link += iteration[j][0]

                    currentElement.value = "<a href=\"" + link + "\">"
                    newNode = tree.Tree()
                    newNode.value = text
                    newNode2 = tree.Tree()
                    while i < len(iteration):
                        if iteration[i][1] == ")":
                            break
                        else:
                            i += 1
                    self.buildTree(iteration[i + 1:], newNode2)
                    currentElement.nodeList.append(newNode)
                    if newNode2.value is not None:
                        newNode.nodeList.append(newNode2)

            elif iteration[0][1] in ("newline", "singlespace", "multispace", "tab", "word", "symbols", "number", "!", "-", "[", "]", "(", ")", "<", ">", "{", "}"):
                newNode = tree.Tree()
                currentElement.value = ""
                items = 0
                for item in iteration:
                    if item[1] in ("newline", "singlespace", "multispace", "tab", "word", "number", "symbols", "!", "-", "[", "]", "(", ")", "<", ">", "{", "}"):
                        currentElement.value += item[0]
                        items += 1
                self.buildTree(iteration[items:], newNode)
                if newNode.value is not None:
                    currentElement.nodeList.append(newNode)
            else:
                return

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

    def number(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "number":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def reference(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "reference":
            self.iteration.append(self.tokens[self.iteration[0]])
            self.iteration[0] += 1
            return True
        else:
            return False

    def top(self):
        if self.iteration[0] > len(self.tokens) - 1: return False
        if self.tokens[self.iteration[0]][1] == "top":
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
        if self.underscore() and self.underscore() and self.wordListWithSpaces() and self.underscore() and self.underscore():
            return True
        elif self.startBoldHTML() and self.wordListWithSpaces() and self.endBoldHTML():
            return True
        else:
            return False

    def bolditalic(self):
        if self.star() and self.star() and self.star() and self.wordListWithSpaces() and self.star() and self.star() and self.star():
            return True
        elif self.startBoldHTML() and self.startItalicHTML() and self.wordListWithSpaces() and self.endItalicHTML() and self.startBoldHTML():
            return True
        elif self.startItalicHTML() and self.startBoldHTML() and self.wordListWithSpaces() and self.endBoldHTML() and self.startItalicHTML():
            return True
        return False

    def strikethrough(self):
        return self.tilde() and self.tilde() and self.wordListWithSpaces() and self.tilde() and self.tilde()

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
        if self.formattedWordList():
            found = False
            while self.verticalLine() or self.formattedWordList():
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

    def formattedWordList(self):
        found = False
        while self.wordListWithSpaces() or self.bold() or self.italic() or self.bolditalic() or self.strikethrough() or self.codeBlock() or self.inlineCode():
            found = True
        return found

    def wordListWithSpaces(self):
        found = False
        while self.word() or self.number() or self.whitespace() or self.symbol() or self.line() or self.tilde() or self.exclamationMark():
            found = True
        return found

    def formatedTextBlock(self):
        found = False
        while self.word() or self.number() or self.whitespace() or self.symbol() or self.line() or self.tilde() or self.newLines() or self.lbrace() or self.rbrace() \
        or self.lparanthesis() or self.rparanthesis() or self.langular() or self.rangular() or self.lbracket() or self.rbracket() or self.startBoldHTML() \
        or self.endBoldHTML() or self.startItalicHTML() or self.endItalicHTML() or self.headings() or self.star() or self.tilde() or self.underscore() \
        or self.verticalLine() or self.exclamationMark():
            found = True
        return found

    def codeBlock(self):
        return self.code() and self.code() and self.code() and self.formatedTextBlock() and self.code() and self.code() and self.code()

    def inlineCode(self):
        return self.code() and self.formatedTextBlock() and self.code()
