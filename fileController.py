from colour import Color

COLORS = [Color("#FFFF00"), #one
        Color("#FFE100"), #two
        Color("#FFC000"), #three
        Color("#FF8E00"), #four
        Color("#FF0000"), #five
        Color("#FF00CE"), #six
        Color("#7030A0"), #seven
        Color("#2532FF"), #eight
        Color("#0070C0"), #nine
        Color("#00B0F0"), #ten
        Color("#00B050"), #eleven
        Color("#92D050"), #twelve
        Color("#FFFFFF")] #thirteen

class CodedLibrary:
    def __init__(self, fileName=None):
        self.wordLib = []
        if (not fileName == None):
            self.wordLib = self.readFile(fileName)
            self.wordLib.sort(key=lambda x: x.word)
    
    def __str__(self):
        tempStr = ""
        for word in self.wordLib:
            tempStr += str(word) + "\n"
        return tempStr

    def __add__(self, otherLib):
        for wordToAdd in otherLib.wordLib:
            notInLib = True
            for word in self.wordLib:
                if (wordToAdd.word == word.word):
                    word.colorArray = word.colorArray + wordToAdd.colorArray
                    word.recalculateColor()
                    notInLib = False
            if (notInLib):
                self.wordLib.append(wordToAdd)
        return self

    def readFile(self, filename):
        filedata = open(filename, "r")
        lines = filedata.readlines()
        wordDict = { "jacob": [11] }
        for line in lines:
            tempVal = line.split("-")[0].split(" ")
            curColor = int(tempVal[0])
            curAmount = int(tempVal[1])
            curWords = line.strip().split("-")[1].split(", ")
            for word in curWords:
                for i in range(curAmount):
                    if word in wordDict:
                        curValues = wordDict[word]
                        curValues.append(curColor)
                        wordDict[word] = curValues
                    else:
                        wordDict[word] = [curColor]
        
        finalLib = []
        for key in wordDict.keys():
            temp = CodedWord(key, wordDict[key])
            finalLib.append(temp)
        return finalLib

    def clearLibrary(self):
        self.wordLib = []

    def replaceLibrary(self, newLib):
        self.wordLib = newLib.wordLib
    
    def atIndex(self, i):
        return self.wordLib[i]
    
    def findWord(self, word):
        for i in range(self.wordLib):
            if self.wordLib[i].word == word:
                return i
        return None
            

class CodedWord(object):
    word = ""
    colorArray = []
    color = None

    def __init__(self, word, color):
        self.word = word.lower()
        self.colorArray = color
        
        tempRed = 0
        tempGreen = 0
        tempBlue = 0
        for j in self.colorArray:
            tempRed = COLORS[j].red + tempRed
            tempGreen = COLORS[j].green + tempGreen
            tempBlue = COLORS[j].blue + tempBlue
        tempColor = Color(rgb=(round(tempRed / len(self.colorArray), 3), round(tempGreen / len(self.colorArray), 3), round(tempBlue / len(self.colorArray), 3)))
        self.color = tempColor
        
    def __str__(self):
        return "{} rgb({}, {}, {}) : {}".format(self.word, round(self.color.red * 255, 3), round(self.color.green * 255, 3), round(self.color.blue * 255, 3), self.colorArray)

    def recalculateColor(self):
        tempRed = 0
        tempGreen = 0
        tempBlue = 0
        for j in self.colorArray:
            tempRed = COLORS[j].red + tempRed
            tempGreen = COLORS[j].green + tempGreen
            tempBlue = COLORS[j].blue + tempBlue
        tempColor = Color(rgb=(round(tempRed / len(self.colorArray), 3), round(tempGreen / len(self.colorArray), 3), round(tempBlue / len(self.colorArray), 3)))
        self.color = tempColor
