
#Calculate number of layers based on number of antennas and BW class
def calculateLayers(layers,mimo,bwClass):
    newLayers = 0
    multiplierFactor = 1

    if bwClass == "b" or bwClass == "c":
        multiplierFactor = 2
    elif bwClass == "d":
        multiplierFactor = 3
    elif bwClass == "e":
        multiplierFactor = 4

    if mimo == "twoLayers":
        newLayers = layers + (2*multiplierFactor)
    elif mimo == "fourLayers":
        newLayers = layers + (4*multiplierFactor)

    return newLayers

def convertBCS(Bcs, wiresharkFormat):
    bcs = ""
    bcsBin = ""

    #Qualcomm format: "111"
    #Wireshark format: "cf"
    if wiresharkFormat:
        for i, bwcs in enumerate(Bcs):
            if   bwcs == "0":  #0000:
                bcsBin = "".join([bcsBin, "{}".format("0000")])
            elif bwcs == "1": #0001
                bcsBin = "".join([bcsBin, "{}".format("0001")])
            elif bwcs == "2": #0010
                bcsBin = "".join([bcsBin, "{}".format("0010")])
            elif bwcs == "3": #0011
                bcsBin = "".join([bcsBin, "{}".format("0011")])
            elif bwcs == "4": #0100
                bcsBin = "".join([bcsBin, "{}".format("0100")])
            elif bwcs == "5": #0101
                bcsBin = "".join([bcsBin, "{}".format("0101")])
            elif bwcs == "6": #0110
                bcsBin = "".join([bcsBin, "{}".format("0110")])
            elif bwcs == "7": #0111
                bcsBin = "".join([bcsBin, "{}".format("0111")])
            elif bwcs == "8": #1000
                bcsBin = "".join([bcsBin, "{}".format("1000")])
            elif bwcs == "9": #1001
                bcsBin = "".join([bcsBin, "{}".format("1001")])
            elif bwcs == "a": #1010
                bcsBin = "".join([bcsBin, "{}".format("1010")])
            elif bwcs == "b": #1011
                bcsBin = "".join([bcsBin, "{}".format("1011")])
            elif bwcs == "c": #1100
                bcsBin = "".join([bcsBin, "{}".format("1100")])
            elif bwcs == "d": #1101
                bcsBin = "".join([bcsBin, "{}".format("1100")])
            elif bwcs == "e": #1110
                bcsBin = "".join([bcsBin, "{}".format("1110")])
            elif bwcs == "f": #1111
                bcsBin = "".join([bcsBin, "{}".format("1111")])
            else:
                print("Unexpected char")
                return
    else:
        bcsBin = Bcs

    for i, bwcs in enumerate(bcsBin):
        if bwcs == "1":
            bcs = "".join([bcs, "BCS_{},".format(i)])

    #Remove last ','
    bcs = bcs[:-1].replace(",","|")
    return(bcs)


def findstring(fileLines, string, StartingPoint):
    for i in range(StartingPoint, len(fileLines)):
        if fileLines[i].find(string) != -1:
            return i


def convertInLine(bandCombinationList):
    combinedInfoList = []
    for items in bandCombinationList:
        combInfo = ""
        for bandCombinationObject in items:
            if combInfo != "":
                combInfo = "".join([combInfo,"_"])
            if bandCombinationObject['SupportedMIMOLayers'] == "fourLayers":
                combInfo = "".join([combInfo,"[{}{}]".format(bandCombinationObject['Band'], bandCombinationObject['BwClass'].upper())])
            else:
                combInfo = "".join([combInfo,"{}{}".format(bandCombinationObject['Band'], bandCombinationObject['BwClass'].upper())])
        combinedInfoList.append(combInfo)
    return combinedInfoList


def convertInStruct(bandList):
    bandCombinationList = []
    for bandString in bandList:
        bandCombination = []
        for item in bandString.split('_'):
            bandElement = {}
            bandElement['SupportedMIMOLayers'] = "twoLayers"
            if '[' in item:
                bandElement['SupportedMIMOLayers'] = "fourLayers"
                bandElement['Band'] = item[1:-2]
                bandElement['BwClass'] = item[-2].lower()
            else:
                bandElement['Band'] = item[:-1]
                bandElement['BwClass'] = item[-1].lower()
            bandCombination.append(bandElement)
        bandCombinationList.append(bandCombination)
    return bandCombinationList
