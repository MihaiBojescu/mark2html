import re


class Tokenizer:
    def __init__(self, buffer):
        self.tokens = []
        self.buffer = buffer

    def tokenize(self):
        oldbuffer = self.buffer
        while self.buffer != "":
            if(self.handleNewline()): continue
            if(self.handleTab()): continue
            if(self.handleSpace()): continue
            if(self.handleMultispace()): continue
            if(self.handleStar()): continue
            if(self.handleUnderscore()): continue
            if(self.handleLine()): continue
            if(self.handleTilde()): continue
            if(self.handleCode()): continue
            if(self.handleVerticalLine()): continue
            if(self.handleExclamationMark()): continue
            if(self.handleHeadings()): continue
            if(self.handleBoldHTML()): continue
            if(self.handleItalicHTML()): continue
            if(self.handleLineBreakHTML()): continue
            if(self.handleParanthesis()): continue
            if(self.handleBrackets()): continue
            if(self.handleAngularBrackets()): continue
            if(self.handleBraces()): continue
            if(self.handleOtherSymbols()): continue
            if(self.handleWords()): continue
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
            return True
        else:
            return False

    def handleTab(self):
        match = re.match("[\t]", self.buffer)
        if match:
            self.addTokenToList(match, "tab")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleMultispace(self):
        match = re.match("[ ]{2,}", self.buffer)
        if match:
            self.addTokenToList(match, "whitespace")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleSpace(self):
        match = re.match("[ ]{1}", self.buffer)
        if match:
            self.addTokenToList(match, "singlespace")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleHeadings(self):
        match = re.match("######", self.buffer)
        if match:
            self.addTokenToList(match, "heading6")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("#####", self.buffer)
        if match:
            self.addTokenToList(match, "heading5")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("####", self.buffer)
        if match:
            self.addTokenToList(match, "heading4")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("###", self.buffer)
        if match:
            self.addTokenToList(match, "heading3")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("##", self.buffer)
        if match:
            self.addTokenToList(match, "heading2")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("#", self.buffer)
        if match:
            self.addTokenToList(match, "heading1")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleParanthesis(self):
        match = re.match("\(", self.buffer)
        if match:
            self.addTokenToList(match, "(")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("\)", self.buffer)
        if match:
            self.addTokenToList(match, ")")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleBrackets(self):
        match = re.match("\[", self.buffer)
        if match:
            self.addTokenToList(match, "[")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("\]", self.buffer)
        if match:
            self.addTokenToList(match, "]")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleAngularBrackets(self):
        match = re.match("[<]", self.buffer)
        if match:
            self.addTokenToList(match, "<")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("[>]", self.buffer)
        if match:
            self.addTokenToList(match, ">")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleBraces(self):
        match = re.match("[\{]", self.buffer)
        if match:
            self.addTokenToList(match, "{")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("[\}]", self.buffer)
        if match:
            self.addTokenToList(match, "}")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleBoldHTML(self):
        match = re.match("<b>", self.buffer)
        if match:
            self.addTokenToList(match, "sbold")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("</b>", self.buffer)
        if match:
            self.addTokenToList(match, "ebold")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleItalicHTML(self):
        match = re.match("<i>", self.buffer)
        if match:
            self.addTokenToList(match, "sitalic")
            self.eliminateTokenFromBuffer(match)
            return True

        match = re.match("</i>", self.buffer)
        if match:
            self.addTokenToList(match, "eitalic")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleLineBreakHTML(self):
        match = re.match("<br>", self.buffer)
        if match:
            self.addTokenToList(match, "linebreak")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleCode(self):
        match = re.match("`", self.buffer)
        if match:
            self.addTokenToList(match, "`")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleStar(self):
        match = re.match("[*]", self.buffer)
        if match:
            self.addTokenToList(match, "*")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleUnderscore(self):
        match = re.match("[_]", self.buffer)
        if match:
            self.addTokenToList(match, "_")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleLine(self):
        match = re.match("[-]", self.buffer)
        if match:
            self.addTokenToList(match, "-")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleTilde(self):
        match = re.match("[~]", self.buffer)
        if match:
            self.addTokenToList(match, "~")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleVerticalLine(self):
        match = re.match("[|]", self.buffer)
        if match:
            self.addTokenToList(match, "|")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleExclamationMark(self):
        match = re.match("[!]", self.buffer)
        if match:
            self.addTokenToList(match, "!")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleOtherSymbols(self):
        match = re.match("[@#$%^&=;:?/.,]+", self.buffer)
        if match:
            self.addTokenToList(match, "symbols")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False

    def handleWords(self):
        match = re.match("[a-zA-Z0-9]+", self.buffer)
        if match:
            self.addTokenToList(match, "word")
            self.eliminateTokenFromBuffer(match)
            return True
        else:
            return False
