
import ExcelHandler
import UtilsLib

print_console = False

bandCombinationList = []
bcUplinkList = []
layersList = []
bcsList = []
bandsList = []
modulationList = []

def parseSupportedBandsV9QualcommFormat(lines):
    supportedBandListV9ndex = -1
    foundV9 = False
    bandListV9 = []
    emptyItem = False
    i = UtilsLib.findstring(lines, "supportedBandListEUTRA-v9")
    for bandV9 in lines[i:]:
        if bandV9.find("supportedBandListEUTRA-v9") != -1:
            supportedBandListV9ndex = bandV9.find("supportedBandListEUTRA-v9")
            foundV9 = True
        elif foundV9 and bandV9.find("{") == supportedBandListV9ndex + 2:
            emptyItem = True
        elif foundV9 and bandV9.find("bandEUTRA-v9") != -1:
            emptyItem = False
            bandLine = lines[i]
            band = bandLine[lines[i].find("bandEUTRA-v9") + len("bandEUTRA-v9   "):None].replace('\n','')
            bandListV9.append(band)
        elif foundV9 and bandV9.find("}") == supportedBandListV9ndex + 2:
            if emptyItem:
                bandListV9.append("")
        elif foundV9 and bandV9.find("}") == supportedBandListV9ndex:
            foundV9 = False
            break
        i += 1
    #Concatenate both supportedBandListEUTRA and supportedBandListEUTRA-v9, replacing  B64 by v9 one
    for i, (j, k) in enumerate(zip(bandsList,bandListV9)):
        if k != "":
            bandsList[i] = bandListV9[i]



def parseSupportedBandsQualcommFormat(lines):
    supportedBandListEUTRAIndex = -1
    foundBandV9 = False
    found = False
    i = UtilsLib.findstring(lines, "supportedBandListEUTRA ")
    for bands in lines[i:]:
        if bands.find("supportedBandListEUTRA") != -1:
            supportedBandListEUTRAIndex = bands.find("supportedBandListEUTRA")
            found = True
        elif found and bands.find("bandEUTRA") != -1:
            bandLine = lines[i]
            band = bandLine[lines[i].find("bandEUTRA") + len("bandEUTRA "):lines[i].find(",")]
            if band == "64":
                foundBandV9 = True
            bandsList.append(band)
        elif found and bands.find("}") == supportedBandListEUTRAIndex:
            found = False
            break
        i += 1
    # Need to add Band Rel9 (B66, B46, B252, B253, B254 and B255)
    if (foundBandV9):
        parseSupportedBandsV9QualcommFormat(lines)



def parseSupportedBandCombinationV10QCATFormat(fileLines):
    item = -1
    foundStart = False
    combo = ""
    mimo = ""
    isCombo = False
    i = UtilsLib.findstring(fileLines, "supportedBandCombination-v1090")
    # where both Band Combination section and Band Combination item begin
    # this will be used to check the end of and item
    band_combination_start_index = -1
    band_combination_item_start_index = -1
    band_combination_band_item_start_index = -1
    bandObj = {}
    bandCombinationItemList = []
    bandCombinationV10List = []
    bandCombinationItemListIndex = 0
    while True:
        # ********************************************* INIT *******************************************************************
        if fileLines[i].find("supportedBandCombination-v1090") != -1:
            foundStart = True
            if (fileLines[i + 1].find("{") != -1):
                band_combination_start_index = fileLines[i + 1].find("{")
                if (fileLines[i + 2].find("{") != -1):
                    band_combination_item_start_index = fileLines[i + 2].find("{")
                    if (fileLines[i + 3].find("{") != -1):
                        band_combination_band_item_start_index = fileLines[i + 3].find("{")
        # ********************************************* ITEM *******************************************************************
        elif foundStart and fileLines[i].find("{") == band_combination_item_start_index:
            item += 1
            bandCombinationItemList = []
            isCombo = False
            bandCombinationItemListIndex = 0
        # ********************************************* BAND ********************************************************************
        # Start new sub-item
        elif foundStart and fileLines[i].find("{") == band_combination_band_item_start_index:
            bandObj = {}
            bandCombinationItemList.append(bandObj)
        elif foundStart and fileLines[i].find("bandEUTRA-v1090") != -1:
            bandLine = fileLines[i]
            band = bandLine[bandLine.find("bandEUTRA-v1090") + len("bandEUTRA-v1090 "):None].replace('\n', '')
            if (isCombo == False):
                combo = "{}".format(band)
            else:
                combo = ''.join([combo, " + {}".format(band)]).replace('\n', '')
            bandCombinationItemList[bandCombinationItemListIndex]['Band'] = band
            bandCombinationItemList[bandCombinationItemListIndex]['Item'] = item
        # ********************************************** Next Item in Combination ***********************************************
        elif foundStart and fileLines[i].find("},") == band_combination_band_item_start_index:
            isCombo = True
            bandCombinationItemListIndex += 1
        # ********************************************** Next Item **************************************************************
        elif foundStart and fileLines[i].find("},") == band_combination_item_start_index:
            bandCombinationV10List.append(bandCombinationItemList)
            if print_console:
                print("Item: {}".format(item))
                if (isCombo):
                    print("Band Combination: {}".format(combo))
                    print("")
                else:
                    combo = combo.replace('\n', '')
                    print("Band: {}".format(combo))
        # ********************************************** END ********************************************************************
        elif foundStart and fileLines[i].find("}") == band_combination_start_index:
            # finish
            bandCombinationV10List.append(bandCombinationItemList)
            if print_console:
                print("Item: {}".format(item))
                if (isCombo):
                    print("Band Combination: {}".format(combo))
                    print("")
                else:
                    combo = combo.replace('\n', '')
                    print("Band: {}".format(combo))
            foundStart = False
            break
        i += 1
    #Need to change order of PCC, as it is already changed in bandCombinationList
    for i, (bcListv10, uplinkOrderList) in enumerate(zip(bandCombinationV10List, bcUplinkList)):
        for j, (bcV10, uplinkList) in enumerate(zip(bcListv10,uplinkOrderList)):
            if j != 0 and uplinkList == True:
                temp = bcListv10[0]
                bcListv10[0] = bcListv10[j]
                bcListv10[j] = temp

    #Concatenate both supportedBandListEUTRA and supportedBandListEUTRA-v9, replacing  B64 by v9 one
    for bcList, bcListv10 in zip(bandCombinationList,bandCombinationV10List):
        for bc, bcV10 in zip(bcList,bcListv10):
            if 'Band' in bcV10 and bcV10['Band'] != int(0):
                bc['Band'] = bcV10['Band']



# QCAT / QXDM format of UE Capability Information message
def parseSupportedBandCombinationQCATFormat(fileLines):
    print("Qualcomm format")
    i = UtilsLib.findstring(fileLines, "supportedBandCombination-r")
    #No Carrier Aggregation support
    if (i == None):
        bandCombinationList.append("None")
        return
    item = -1
    foundStart = False
    combo = ""
    mimo = ""
    isCombo = False
    #where both Band Combination section and Band Combination item begin
    #this will be used to check the end of and item
    band_combination_start_index = -1
    band_combination_item_start_index = -1
    band_combination_band_item_start_index = -1
    foundBandCOmbinationV10 = False
    layers = 0
    mimoList = []
    bwClass = ""
    hasUplink = False
    mimoListIndex = 0
    bandObj = {}
    bandCombinationItemList = []
    bandCombinationUplinkList = []
    bandCombinationItemListIndex = 0
    while True:
# ********************************************* INIT *******************************************************************
        if fileLines[i].find("supportedBandCombination-r10") != -1:
            foundStart = True
            if (fileLines[i+1].find("{") != -1):
                band_combination_start_index = fileLines[i+1].find("{")
                if (fileLines[i+2].find("{") != -1):
                    band_combination_item_start_index = fileLines[i+2].find("{")
                    if (fileLines[i+3].find("{") != -1):
                        band_combination_band_item_start_index = fileLines[i+3].find("{")
# ********************************************* ITEM *******************************************************************
        elif foundStart and fileLines[i].find("{") == band_combination_item_start_index:
            item += 1
            bandCombinationItemList = []
            bandCombinationUplinkList = []
            isCombo = False
            layers = 0
            mimoListIndex = 0
            bandCombinationItemListIndex = 0
            mimoList = []
#********************************************* BAND ********************************************************************
        #Start new sub-item
        elif foundStart and fileLines[i].find("{") == band_combination_band_item_start_index:
            bandObj = {}
            bandCombinationItemList.append(bandObj)
        elif foundStart and fileLines[i].find("bandEUTRA-r10") != -1:
            bandLine = fileLines[i]
            band = bandLine[bandLine.find("bandEUTRA-r10") + len("bandEUTRA-r10 "):fileLines[i].find(",")]
            if band == "64":
                foundBandCOmbinationV10 = True
            if (isCombo == False):
                combo = "{}".format(band)
            bandCombinationItemList[bandCombinationItemListIndex]['Band'] = band
            bandCombinationItemList[bandCombinationItemListIndex]['Item'] = item
            if fileLines[i + 1].find("bandParametersUL-r10") != -1:
                hasUplink = True
                bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = True
                bandCombinationUplinkList.append(True)
            else:
                hasUplink = False
                bandCombinationUplinkList.append(False)
#********************************************* MIMO ********************************************************************
        elif fileLines[i].find("supportedMIMO-CapabilityDL-r10") != -1:
            #get number of supported antennas
            mimoLine = fileLines[i]
            mimo = mimoLine[fileLines[i].find("supportedMIMO-CapabilityDL-r10") + len("supportedMIMO-CapabilityDL-r10 "):None].replace('\n','')
            bandCombinationItemList[bandCombinationItemListIndex]['SupportedMIMOLayers'] = mimo
            if fileLines[i-1].find("ca-BandwidthClassDL-r10") != -1:
                #get bandwidth class
                bwClassStart = fileLines[i-1].find("ca-BandwidthClassDL-r10") + len("ca-BandwidthClassDL-r10 ")
                bwLine = fileLines[i-1]
                bwClass = bwLine[bwClassStart:bwClassStart+1]
                bandCombinationItemList[bandCombinationItemListIndex]['BwClass'] = bwClass
                if isCombo:
                    if hasUplink:
                        # this is the main band, as contains UL
                        combo = ''.join(["{}{} + ".format(band,bwClass.upper()), combo]).replace('\n', '')
                        mimoList.insert(mimoListIndex-1,mimo)
                        bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = True
                        temp = bandCombinationItemList[bandCombinationItemListIndex]                        #
                        bandCombinationItemList[bandCombinationItemListIndex] = bandCombinationItemList[0]  #Swap Uplink
                        bandCombinationItemList[0] = temp                                                   #
                    else:
                        combo = ''.join([combo, " + {}{}".format(band,bwClass.upper())]).replace('\n', '')
                        mimoList.insert(mimoListIndex,mimo)
                        bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = False
                else:
                    combo = ''.join([combo, "{}".format(bwClass.upper())]).replace('\n', '')
                    mimoList.insert(mimoListIndex-1, mimo)
                mimoListIndex += 1
                layers = UtilsLib.calculateLayers(layers, mimo, bwClass)
#********************************************** Next Item in Combination ***********************************************
        elif foundStart and fileLines[i].find("},") == band_combination_band_item_start_index:
            isCombo = True
            bandCombinationItemListIndex += 1
#********************************************** Next Item **************************************************************
        elif foundStart and fileLines[i].find("},") == band_combination_item_start_index:
            bandCombinationList.append(bandCombinationItemList)
            bcUplinkList.append(bandCombinationUplinkList)
            layersList.append(layers)
            if print_console:
                print("Item: {}".format(item ))
                if (isCombo):
                    print("Band Combination: {}".format(combo))
                    print("Layers: {}".format(layers))
                    print("MIMO: {}".format(mimoList).replace('[', '').replace(']', '').replace('\'', '').replace('\n', ''))
                    print("")
                else:
                    combo = combo.replace('\n', '')
                    print("Band: {}".format(combo))
                    print("MIMO: {}".format(mimo))
                    if bwClass == "b" or bwClass == "c" or bwClass == "d" or bwClass == "e":
                        print("Layers: {}\n".format(layers))
                    else:
                        print("")
#********************************************** END ********************************************************************
        elif foundStart and fileLines[i].find("}") == band_combination_start_index:
            #finish
            bandCombinationList.append(bandCombinationItemList)
            bcUplinkList.append(bandCombinationUplinkList)
            layersList.append(layers)
            if print_console:
                print("Item: {}".format(item - 1))
                if (isCombo):
                    print("Band Combination: {}".format(combo))
                    print("Layers: {}".format(layers))
                    print("MIMO: {}".format(mimoList).replace('[','').replace(']','').replace('\'','').replace('\n', ''))
                    print("")
                else:
                    combo = combo.replace('\n', '')
                    print("Band: {}".format(combo))
                    print("MIMO: {}".format(mimo).replace('\n', ''))
                    if bwClass == "b" or bwClass == "c" or bwClass == "d" or bwClass == "e":
                        print("Layers: {}\n".format(layers))
                    else:
                        print("")
            foundStart = False
            break
        i += 1
    #Handle supportedBandCombination-v1090
    if foundBandCOmbinationV10:
        parseSupportedBandCombinationV10QCATFormat(fileLines)


def parseBandwidthCombinationSetQualcommFormat(fileLines):

    i = UtilsLib.findstring(fileLines, "supportedBandCombinationExt-r")

    #no Carrier Aggregation support
    if (i == None):
        bcsList.append("None")
        return

    foundStart = False
    bandwidth_combination_set_start_index = -1
    bandwidth_combination_set_item_start_index = -1
    bandwidth_combination_set_item = -1
    BCSExpected = False

    while True:
        # ********************************************* INIT *******************************************************************
        if fileLines[i].find("supportedBandCombinationExt-r10") != -1:
            foundStart = True
            if (fileLines[i+1].find("{") != -1):
                bandwidth_combination_set_start_index = fileLines[i+1].find("{")
                if (fileLines[i + 2].find("{") != -1):
                    bandwidth_combination_set_item_start_index = fileLines[i + 2].find("{")
        elif foundStart and fileLines[i].find("{") == bandwidth_combination_set_item_start_index:
            bandwidth_combination_set_item += 1
            BCSExpected = True
        elif foundStart and fileLines[i].find("}") == bandwidth_combination_set_item_start_index:
                if BCSExpected:
                    bcsList.append("")
        elif foundStart and fileLines[i].find("supportedBandwidthCombinationSet-r10") != -1:
            bcsLine = fileLines[i]
            bcs = bcsLine[fileLines[i].find("supportedBandwidthCombinationSet-r10") + len("supportedBandwidthCombinationSet-r10 \'"):fileLines[i].find("\'B")]
            bcsList.append(UtilsLib.convertBCS(bcs.lower(),False))
            BCSExpected = False
        elif foundStart and fileLines[i].find("}") == bandwidth_combination_set_start_index:
            foundStart = False
            break
        i += 1



def parseHighOrderModulationQualcommFormat(lines):
    supportedModulationEUTRAIndex = -1
    dicMod = {}
    found = False
    for i, bands in enumerate(lines):
        if bands.find("supportedBandListEUTRA-v1250 ") != -1:
            supportedModulationEUTRAIndex = bands.find("supportedBandListEUTRA-v1250 ")
            found = True
        elif found and bands.find("dl-256QAM-r12") != -1:
            dicMod = {}
            modLine = lines[i]
            downlink = modLine[lines[i].find("dl-256QAM-r12") + len("dl-256QAM-r12 "):lines[i].find(",")]
            dicMod['dl-256QAM-r12'] = downlink
        elif found and bands.find("ul-64QAM-r12") != -1:
            modLine = lines[i]
            uplink = modLine[lines[i].find("ul-64QAM-r12") + len("ul-64QAM-r12 "):None].replace('\n','')
            dicMod['ul-64QAM-r12'] = uplink
            modulationList.append(dicMod)
        elif found and bands.find("}") == supportedModulationEUTRAIndex:
            break
    #if there is no support for 256QAM or 64QAM
    if found == False:
        for band in enumerate(bandsList):
            modList = []
            dicMod = {}
            dicMod['dl-256QAM-r12'] = "not supported"
            dicMod['ul-64QAM-r12'] = "not supported"
            modulationList.append(dicMod)


#************* Called from main loop. This method will call all other parsers and will store data in DB*****************
def parseQualcommFormat(lines, fileName):
    #Parse supported LTE bands
    parseSupportedBandsQualcommFormat(lines)

    #Parse supported band combination
    parseSupportedBandCombinationQCATFormat(lines)

    #parse supported BCS
    parseBandwidthCombinationSetQualcommFormat(lines)

    #parse support for 256QAM in DL and 64QAM in UL
    parseHighOrderModulationQualcommFormat(lines)

    #write table on Excel
    ExcelHandler.write2Excel(bandsList, bandCombinationList, layersList, bcsList, modulationList, fileName)