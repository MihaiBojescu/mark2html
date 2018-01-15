import re


class Tokenizer:
    def __init__(self, buffer):
        self.tokens = []
        self.buffer = buffer

    def tokenize(self):
        oldbuffer = self.buffer
        while(self.buffer != ""):
            self.handleNewline()
            self.handleTab()
            self.handleSpace()
            self.handleMultispace()
            self.handleStar()
            self.handleUnderscore()
            self.handleLine()
            self.handleTilde()
            self.handleCode()
            self.handleHeadings()
            self.handleBoldHTML()
            self.handleLineBreakHTML()
            self.handleParanthesis()
            self.handleBrackets()
            self.handleAngularBrackets()
            self.handleBraces()
            self.handleOtherSymbols()
            self.handleWords()
            if(oldbuffer == self.buffer):
                print("\n\nGot stuck at \"" + self.buffer.split(' ', 1)[0] + "\"")
                print("Rest of buffer is:\n" + self.buffer)
                break
            oldbuffer = self.buffer

    def getTokens(self):
        return self.tokens

    def addTokenToList(self, token, type):
        # print("Found token: type: \"" + type + "\" token: \"" + token.group(0) + "\"")
        self.tokens.append((token.group(0), type))

    def eliminateTokenFromBuffer(self, token):
        self.buffer = self.buffer[len(token.group(0)):]

    def handleNewline(self):
        match = re.match("[\n]", self.buffer)
        if match:
            self.addTokenToList(match, "newline")
            self.eliminateTokenFromBuffer(match)

    def handleTab(self):
        match = re.match("[\t]", self.buffer)
        if match:
            self.addTokenToList(match, "tab")
            self.eliminateTokenFromBuffer(match)

    def handleMultispace(self):
        match = re.match("[ ]{2,}", self.buffer)
        if match:
            self.addTokenToList(match, "whitespace")
            self.eliminateTokenFromBuffer(match)

    def handleSpace(self):
        match = re.match("[ ]{1}", self.buffer)
        if match:
            self.addTokenToList(match, "singlespace")
            self.eliminateTokenFromBuffer(match)

    def handleHeadings(self):
        match = re.match("######", self.buffer)
        if match:
            self.addTokenToList(match, "heading6")
            self.eliminateTokenFromBuffer(match)

        match = re.match("#####", self.buffer)
        if match:
            self.addTokenToList(match, "heading5")
            self.eliminateTokenFromBuffer(match)

        match = re.match("####", self.buffer)
        if match:
            self.addTokenToList(match, "heading4")
            self.eliminateTokenFromBuffer(match)

        match = re.match("###", self.buffer)
        if match:
            self.addTokenToList(match, "heading3")
            self.eliminateTokenFromBuffer(match)

        match = re.match("##", self.buffer)
        if match:
            self.addTokenToList(match, "heading2")
            self.eliminateTokenFromBuffer(match)

        match = re.match("#", self.buffer)
        if match:
            self.addTokenToList(match, "heading1")
            self.eliminateTokenFromBuffer(match)

    def handleParanthesis(self):
        match = re.match("\(", self.buffer)
        if match:
            self.addTokenToList(match, "(")
            self.eliminateTokenFromBuffer(match)

        match = re.match("\)", self.buffer)
        if match:
            self.addTokenToList(match, ")")
            self.eliminateTokenFromBuffer(match)

    def handleBrackets(self):
        match = re.match("\[", self.buffer)
        if match:
            self.addTokenToList(match, "[")
            self.eliminateTokenFromBuffer(match)

        match = re.match("\]", self.buffer)
        if match:
            self.addTokenToList(match, "]")
            self.eliminateTokenFromBuffer(match)

    def handleAngularBrackets(self):
        match = re.match("[<]", self.buffer)
        if match:
            self.addTokenToList(match, "langular")
            self.eliminateTokenFromBuffer(match)

        match = re.match("[>]", self.buffer)
        if match:
            self.addTokenToList(match, "rangular")
            self.eliminateTokenFromBuffer(match)
            self.eliminateTokenFromBuffer(match)

    def handleBraces(self):
        match = re.match("[\{]", self.buffer)
        if match:
            self.addTokenToList(match, "lbrace")
            self.eliminateTokenFromBuffer(match)

        match = re.match("[\}]", self.buffer)
        if match:
            self.addTokenToList(match, "rbrace")
            self.eliminateTokenFromBuffer(match)

    def handleBoldHTML(self):
        match = re.match("<b>", self.buffer)
        if match:
            self.addTokenToList(match, "sbold")
            self.eliminateTokenFromBuffer(match)

        match = re.match("</b>", self.buffer)
        if match:
            self.addTokenToList(match, "ebold")
            self.eliminateTokenFromBuffer(match)

    def handleLineBreakHTML(self):
        match = re.match("<br>", self.buffer)
        if match:
            self.addTokenToList(match, "linebreak")
            self.eliminateTokenFromBuffer(match)

    def handleCode(self):
        match = re.match("`", self.buffer)
        if match:
            self.addTokenToList(match, "code")
            self.eliminateTokenFromBuffer(match)

    def handleStar(self):
        match = re.match("[*]", self.buffer)
        if match:
            self.addTokenToList(match, "star")
            self.eliminateTokenFromBuffer(match)

    def handleUnderscore(self):
        match = re.match("[_]", self.buffer)
        if match:
            self.addTokenToList(match, "underscore")
            self.eliminateTokenFromBuffer(match)

    def handleLine(self):
        match = re.match("[-]", self.buffer)
        if match:
            self.addTokenToList(match, "line")
            self.eliminateTokenFromBuffer(match)

    def handleTilde(self):
        match = re.match("[~]", self.buffer)
        if match:
            self.addTokenToList(match, "tilde")
            self.eliminateTokenFromBuffer(match)

    def handleOtherSymbols(self):
        match = re.match("[@!#$%^&=;:<?/.,]+", self.buffer)
        if match:
            self.addTokenToList(match, "symbols")
            self.eliminateTokenFromBuffer(match)

    def handleWords(self):
        match = re.match("[a-zA-Z0-9]+", self.buffer)
        if match:
            self.addTokenToList(match, "word")
            self.eliminateTokenFromBuffer(match)
