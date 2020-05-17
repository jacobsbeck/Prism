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

    # A Coded Library takes a filename and creates a list of word 
    # objects read in from the given file.
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

    # This method takes a filename and reads the file data in coded word 
    # objects that are then added to the word libaray.
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

    # This method clears the current word library.
    def clearLibrary(self):
        self.wordLib = []

    # This method takes a word library and replaces the current one with the new library.
    def replaceLibrary(self, newLib):
        self.wordLib = newLib.wordLib
    
    # This method takes a index and returns the word value at that given index.
    def atIndex(self, i):
        return self.wordLib[i]
    
    # This method takes a word and rreturn the index of that word, 
    # if it can't be found return none.
    def findWord(self, word):
        for i in range(self.wordLib):
            if self.wordLib[i].word == word:
                return i
        return None
            

class CodedWord(object):
    word = ""
    colorArray = []
    color = None

    # A Coded Word takes a string that is the word and an array of 
    # colors that represent that word read in from the file.
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

    # This method looks at the color array of the coded word and 
    # calculates it's color by mixing the colors together.
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

class CodedColor(object):
    colorName = ""
    colorRGB = [0, 0, 0]
    color = None

    # A Coded Color takes a string that is the color name and an rgb array.
    def __init__(self, color_name, rgb):
        self.colorName = color_name
        self.colorRGB = [round(int(rgb[0]) / 255, 3), round(int(rgb[1]) / 255, 3), round(int(rgb[2]) / 255, 3)]
        self.color = Color(rgb=(self.colorRGB[0], self.colorRGB[1], self.colorRGB[2]))

    
    def __str__(self):
        return "rgb({}, {}, {}) : {}".format(round(self.color.red * 255, 3), round(self.color.green * 255, 3), round(self.color.blue * 255, 3), self.colorName)

class ColorLibrary:
    colorLib = []

    # A Color Library takes a filename and creates a list of color 
    # objects read in from the given file.
    def __init__(self, fileName=None):
        if (not fileName == None):
            self.colorLib = self.readFile(fileName)
    
    def __str__(self):
        tempStr = ""
        for color in self.colorLib:
            tempStr += str(color) + "\n"
        return tempStr

    # This method takes a filename and reads the file data in coded color 
    # objects that are then added to the color libaray.
    def readFile(self, filename):
        filedata = open(filename, "r")
        lines = filedata.readlines()
        tempLib = []
        for line in lines:
            lineValues = line.split(" ")
            newColor = CodedColor(lineValues[0].replace("_", " "), lineValues[2].replace("(", "").replace(")", "").split(","))
            tempLib.append(newColor)
        return tempLib
    
class Prompts:
    prompts = []

    # A Color Library takes a filename and creates a list of color 
    # objects read in from the given file.
    def __init__(self, fileName=None):
        if (not fileName == None):
            self.prompts = self.readFile(fileName)
    
    def __str__(self):
        tempStr = ""
        for color in self.prompts:
            tempStr += str(color) + "\n"
        return tempStr

    # This method takes a filename and reads the file data in coded color 
    # objects that are then added to the color libaray.
    def readFile(self, filename):
        filedata = open(filename, "r")
        lines = filedata.readlines()
        return lines
