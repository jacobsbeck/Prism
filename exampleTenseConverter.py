from pyinflect import getAllInflections, getInflection

#inflect = getAllInflections('Arousal')
#for  x in inflect:
#    for i in inflect[x]:
#        print (i)

   
def readFile(filename):
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
        curInflect = []
        inflect = getAllInflections(key)
        for l in inflect:
            for i in inflect[l]:
                if not i in curInflect:
                    curInflect.append(i)
                    print(i)
                    #temp = CodedWord(key, inflect[i])
                    #finalLib.append(temp)
    return finalLib

readFile("allCodedWords.txt")