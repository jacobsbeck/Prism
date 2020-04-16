from colour import Color
WORD_LIB = []

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


def readFile(filename):
    filedata = open(filename, "r")
    lines = filedata.readlines()
    word_dict = { "jacob": [11] }
    for line in lines:
        d = line.strip().split(" ")
        if d[0] in word_dict:
            cur_key_values = word_dict[d[0]]
            cur_key_values.append(d[1])
            word_dict[d[0]] = cur_key_values
        else:
            word_dict[d[0]] = [d[1]]
    
    for key in word_dict.keys():
        temp = CodedWord(key, word_dict[key])
        WORD_LIB.append(temp)
    
    for word in WORD_LIB:
        print(word)

class CodedWord(object):
    word = ""
    color_array = []
    color = None

    def __init__(self, word, color):
        self.word = word.lower()
        self.color_array = color

        number_colors = 13
        index_check = []
        for i in range(number_colors):
            index_check.append(False)
        for color_index in self.color_array:
            index_check[int(color_index) - 1] = True
        tempColor = None
        for j in range(len(index_check)):
            if index_check[j]:
                if tempColor is None:
                    tempColor = COLORS[j]
                else:
                    tempRed = round((tempColor.red + COLORS[j].red) / 2.0, 3)
                    tempGreen = round((tempColor.green + COLORS[j].green) / 2.0, 3)
                    tempBlue = round((tempColor.blue + COLORS[j].blue) / 2.0, 3)
                    tempColor = Color(rgb=(tempRed, tempGreen, tempBlue))
        self.color = tempColor
    
    def __str__(self):
        return " {} rgb({}, {}, {}) : {}".format(self.word, round(self.color.red * 255, 3), round(self.color.green * 255, 3), round(self.color.blue * 255, 3), self.color_array)

readFile("codedWords.txt")