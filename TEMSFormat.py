
import ExcelHandler
import UtilsLib

bandCombinationList = []
bcUplinkList = []
layersList = []
bcsList = []
bandsList = []
modulationList = []

def parseSupportedBandsV9TEMSFormat(lines):
    bandListV9 = []
    foundV9 = False
    for i, bandV9 in enumerate(lines):
        if bandV9.find("supportedBandListEUTRA-v9") != -1:
            foundV9 = True
        elif foundV9 and bandV9.find('[') != -1:
            bandLine = lines[i+1]
            if bandLine.find('bandEUTRA-v9') == -1:
                bandListV9.append("")
        elif foundV9 and bandV9.find("bandEUTRA-v9") != -1:
            bandLine = lines[i]
            band = bandLine[lines[i].find(":") + 2:None].replace('\n','')
            bandListV9.append(band)
        elif foundV9 and bandV9.find("nonCriticalExtension") != -1:
            foundV9 = False
            break
    #Concatenate both supportedBandListEUTRA and supportedBandListEUTRA-v9, replacing  B64 by v9 one
    for i, (j, k) in enumerate(zip(bandsList,bandListV9)):
        if k != "":
            bandsList[i] = bandListV9[i]



def parseSupportedBandsTEMSFormat(lines):
    found = False
    foundBandV9 = False
    for i, bands in enumerate(lines):
        if bands.find("SupportedBandListEUTRA :") != -1:
            found = True
        elif found and bands.find("bandEUTRA :") != -1:
            bandLine = lines[i]
            band = bandLine[lines[i].find("bandEUTRA :") + len("bandEUTRA : "):None].replace('\n','')
            if band == "64":
                foundBandV9 = True
            bandsList.append(band)
        elif found and bands.find("measParameters") != -1:
            found = False
            break
    # Need to add Band Rel9 (B66, B46, B252, B253, B254 and B255)
    if (foundBandV9):
        parseSupportedBandsV9TEMSFormat(lines)

    # Check if device support NR
    i = UtilsLib.findstring(lines, "en-DC-r15: supported")
    if i is not None:
        foundBandNR = False
        for i, bandNR in enumerate(lines):
            if bandNR.find("SupportedBandListNR-r15 :") != -1:
                foundBandNR = True
            elif foundBandNR and bandNR.find("bandNR-r15 :") != -1:
                bandLine = lines[i]
                band = bandLine[lines[i].find("bandNR-r15 :") + len("bandNR-r15 : "):None].replace('\n', '')
                band = ''.join((band, 'n'))
                bandsList.append(band)
            elif foundBandNR and bandNR.find("featureSetsEUTRA-r15") != -1:
                foundBandNR = False

                break

def parseBandCombinationV10TEMSFormat(fileLines):
    item = 0
    comboItem = 0
    foundStart = False
    combo = ""
    isCombo = False
    band_combination_item_start_index = -1
    band_item_Index = -1
    bandObj = {}
    bandCombinationItemList = []
    bandCombinationV10List = []
    bandCombinationItemListIndex = 0
    subItem = -1
    i = UtilsLib.findstring(fileLines, "SupportedBandCombination-v1090 :")
    while True:
        # ********************************************* INIT ***********************************************************
        if not foundStart and fileLines[i].find("SupportedBandCombination-v1090 :") != -1:
            foundStart = True
            if fileLines[i + 1].find("[") != -1:
                band_combination_item_start_index = fileLines[i + 1].find("[")
                if fileLines[i + 2].find("BandCombinationParameters-v1090") != -1:
                    if fileLines[i + 3].find("[") != -1:
                        band_item_Index = fileLines[i + 3].find("[")

        # ********************************************* ITEM ***********************************************************
        elif foundStart and fileLines[i].find('[') == band_combination_item_start_index:
            # in case there is no bandEUTRA-v1090, subItem will be different from -1, so, we need to append anyway
            if subItem != -1:
                bandCombinationV10List.append(bandCombinationItemList)
            bandCombinationItemListIndex = -1
            bandCombinationItemList = []
            isCombo = False
            subItem = -1
            combo = ""
        elif foundStart and fileLines[i].find('[') == band_item_Index:
            if (fileLines[i + 1].find("bandEUTRA-v1090") != -1 and fileLines[i + 2].find("[") == band_item_Index) \
                    or fileLines[i + 1].find("[") == band_item_Index:
                isCombo = True
                ComboLine = fileLines[i]
                comboItem = ComboLine[ComboLine.find('[') + 1: ComboLine.find(']')].replace(' ', '')
            bandObj = {}
            bandCombinationItemList.append(bandObj)
            bandCombinationItemListIndex += 1
            subItem += 1
        # ********************************************* BAND ***********************************************************
        elif foundStart and fileLines[i].find("bandEUTRA-v1090 :") != -1:
            bandLine = fileLines[i]
            band = bandLine[bandLine.find("bandEUTRA-v1090") + len("bandEUTRA-v1090 : "):None].replace('\n', '').replace(' ', '')
            if isCombo:
                combo = ''.join([combo, " + {}".format(band)]).replace('\n', '')
            else:
                combo = "{}".format(band)
            bandCombinationItemList[bandCombinationItemListIndex]['Band'] = band
            if comboItem == subItem:
                bandCombinationV10List.append(bandCombinationItemList)
                subItem = -1
        # ********************************************** END ***********************************************************
        elif fileLines[i].find("nonCriticalExtension") != -1:
            # finish
            bandCombinationV10List.append(bandCombinationItemList)
            foundStart = False
            break
        i += 1
    # Need to change order of PCC, as it is already changed in bandCombinationList
    for i, (bcListv10, uplinkOrderList) in enumerate(zip(bandCombinationV10List, bcUplinkList)):
        for j, (bcV10, uplinkList) in enumerate(zip(bcListv10,uplinkOrderList)):
            if j != 0 and uplinkList == True:
                temp = bcListv10[0]
                bcListv10[0] = bcListv10[j]
                bcListv10[j] = temp

    # Concatenate both supportedBandListEUTRA and supportedBandListEUTRA-v9, replacing  B64 by v9 one
    for bcList, bcListv10 in zip(bandCombinationList,bandCombinationV10List):
        for bc, bcV10 in zip(bcList,bcListv10):
            if bc['Band'] == "64":
                if 'Band' in bcV10 and bcV10['Band'] != int(0):
                    bc['Band'] = bcV10['Band']


# Wireshark format of UE Capability Information message
def parseBandCombinationTEMSFormat(fileLines):
    print("TEMS Format")
    bandDic = {'supportedBandCombination-r10':
                {'SupportedBandCombination': 'SupportedBandCombination-r10 : ',
                    'bandEUTRA': 'bandEUTRA-r10',
                    'BandParametersUL': 'BandParametersUL-r10',
                    'supportedMIMO-CapabilityDL': 'SupportedMIMO-CapabilityDL-r10 : ',
                    'ca-BandwidthClassDL': 'ca-BandwidthClassDL-r10 : ',
                    'supportedBandwidthCombinationSet' : 'This item is not available on this revision',
                    'End': 'measParameters-v1020'},
               'supportedBandCombinationReduced-r13':
                   {'SupportedBandCombination': 'SupportedBandCombinationReduced-r13 : ',
                    'bandEUTRA': 'bandEUTRA-r13',
                    'BandParametersUL': 'BandParametersUL-r13',
                    'supportedMIMO-CapabilityDL': 'supportedMIMO-CapabilityDL-r13 : ',
                    'ca-BandwidthClassDL': 'ca-BandwidthClassDL-r13 : ',
                    'supportedBandwidthCombinationSet' : 'supportedBandwidthCombinationSet-r13',
                    'End': 'measParameters-v1310'}
               }
    # Check which 3GPP revision is been used, and if none, return
    if UtilsLib.findstring(fileLines, "supportedBandCombination-r10") is not None:
        revisionSupport = 'supportedBandCombination-r10'
        i = UtilsLib.findstring(fileLines, "supportedBandCombination-r10")
    elif UtilsLib.findstring(fileLines, "supportedBandCombinationReduced-r13") is not None:
        i = UtilsLib.findstring(fileLines, "supportedBandCombinationReduced-r13")
        revisionSupport = 'supportedBandCombinationReduced-r13'
    else:
        bandCombinationList.append("None")
        return

    item = 0
    band = 0
    foundStart = False
    previousItem = -1
    combo = ""
    mimo = ""
    isCombo = False
    band_combination_item_start_index = -1
    layers = 0
    mimoList = []
    bwClass = ""
    hasUplink = False
    mimoListIndex = 0
    bandObj = {}
    bandCombinationItemList = []
    bandCombinationUplinkList = []
    bandCombinationItemListIndex = 0
    foundBandCombinationV10 = False
    foundBandWidthCombinationSetV13 = False
    while True:
# ********************************************* INIT *******************************************************************
        if fileLines[i].find(bandDic[revisionSupport]['SupportedBandCombination']) != -1:
            foundStart = True
            if (fileLines[i+1].find("[") != -1):
                band_combination_item_start_index = fileLines[i+1].find("[")
# ********************************************* ITEM *******************************************************************
        elif foundStart and fileLines[i].find("[") == band_combination_item_start_index:
            itemLine = fileLines[i]
            item = int(itemLine[fileLines[i].find("[") + len("["):None].replace(']', '').replace(': ', ''))
            if revisionSupport is 'supportedBandCombinationReduced-r13':
                bcsList.append("")
# ********************************************* BAND *******************************************************************
        elif foundStart and fileLines[i].find(bandDic[revisionSupport]['bandEUTRA']) != -1:
            # get supported bands
            bandLine = fileLines[i]
            band = bandLine[bandLine.find(bandDic[revisionSupport]['bandEUTRA']) +
                            len(bandDic[revisionSupport]['bandEUTRA'] + ": "):None].replace('\n', '').replace(' ', '')
            if band is "64":
                foundBandCombinationV10 = True
            bandObj = {}
            if item != previousItem:
                # new Item found
                if combo != "":
                    bandCombinationList.append(bandCombinationItemList)
                    bcUplinkList.append(bandCombinationUplinkList)
                    layersList.append(layers)
                    # bandCombinationList.append(layers)
                isCombo = False
                layers = 0
                mimoListIndex = 0
                bandCombinationItemListIndex = 0
                bandCombinationItemList = []
                bandCombinationUplinkList = []
                mimoList = []
                previousItem = item
                combo = "{}".format(band)
            else:
                isCombo = True
            bandCombinationItemList.append(bandObj)
            bandCombinationItemList[bandCombinationItemListIndex]['Band'] = band
            bandCombinationItemList[bandCombinationItemListIndex]['Item'] = item
            if fileLines[i + 2].find(bandDic[revisionSupport]['BandParametersUL']) != -1:
                hasUplink = True
                bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = True
                bandCombinationUplinkList.append(True)
            else:
                hasUplink = False
                bandCombinationUplinkList.append(False)
# ********************************************* MIMO *******************************************************************
        elif fileLines[i].find(bandDic[revisionSupport]['supportedMIMO-CapabilityDL']) != -1:
            # get number of supported antennas
            mimoLine = fileLines[i]
            mimo = mimoLine[fileLines[i].find(bandDic[revisionSupport]['supportedMIMO-CapabilityDL']) +
                            len(bandDic[revisionSupport]['supportedMIMO-CapabilityDL']):]
            bandCombinationItemList[bandCombinationItemListIndex]['SupportedMIMOLayers'] = mimo
            if fileLines[i-1].find(bandDic[revisionSupport]['ca-BandwidthClassDL']) != -1:
                # get bandwidth class
                bwClassStart = fileLines[i-1].find(bandDic[revisionSupport]['ca-BandwidthClassDL']) + \
                               len(bandDic[revisionSupport]['ca-BandwidthClassDL'])
                bwLine = fileLines[i-1]
                bwClass = bwLine[bwClassStart:bwClassStart+1]
                bandCombinationItemList[bandCombinationItemListIndex]['BwClass'] = bwClass
                if isCombo:
                    if hasUplink:
                        # this is the main band, as contains UL
                        combo = ''.join(["{}{} + ".format(band, bwClass.upper()), combo]).replace('\n', '')
                        mimoList.insert(mimoListIndex-1, mimo)
                        bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = True
                        temp = bandCombinationItemList[bandCombinationItemListIndex]                        #
                        bandCombinationItemList[bandCombinationItemListIndex] = bandCombinationItemList[0]  #Swap Uplink
                        bandCombinationItemList[0] = temp                                                   #
                    else:
                        combo = ''.join([combo, " + {}{}".format(band, bwClass.upper())]).replace('\n', '')
                        mimoList.insert(mimoListIndex, mimo)
                        bandCombinationItemList[bandCombinationItemListIndex]['HasUplink'] = False
                else:
                    combo = ''.join([combo, "{}".format(bwClass.upper())]).replace('\n', '')
                    mimoList.insert(mimoListIndex - 1, mimo)
                mimoListIndex += 1
                layers = UtilsLib.calculateLayers(layers, mimo, bwClass)
            bandCombinationItemListIndex += 1
# ************************************** Supported Bandwidth Combination Set *******************************************
        elif fileLines[i].find(bandDic[revisionSupport]['supportedBandwidthCombinationSet']) != -1:
            bcsLine = fileLines[i+1]
            bcs = bcsLine[fileLines[i+1].find('Binary string (Bin) : ') + len('Binary string (Bin) :'):].strip()
            print("Item: " + str(item))
            print("Size of bcList: " + str(len(bcsList)))
            bcsList[item] = UtilsLib.convertBCS(bcs, False)
# ********************************************* END ********************************************************************
        elif fileLines[i].find(bandDic[revisionSupport]['End']) != -1:
            # finish
            bandCombinationList.append(bandCombinationItemList)
            bcUplinkList.append(bandCombinationUplinkList)
            layersList.append(layers)
            foundStart = False
            break
        i += 1
    # Handle supportedBandCombination-v1090
    if foundBandCombinationV10:
        parseBandCombinationV10TEMSFormat(fileLines)


def parseBandwidthCombinationSetTEMSFormat(fileLines):

    i = UtilsLib.findstring(fileLines, "SupportedBandCombinationExt-r10 :")

    # no Carrier Aggregation support
    if i is None:
        bcsList.append("None")
        return

    foundStart = False
    bandwidth_combination_set_item_start_index = -1

    while True:
        # ********************************************* INIT ***********************************************************
        if fileLines[i].find("SupportedBandCombinationExt-r10 :") != -1:
            foundStart = True
            if fileLines[i+1].find("[") != -1:
                bandwidth_combination_set_item_start_index = fileLines[i+1].find("[")
        elif foundStart and fileLines[i].find("[") == bandwidth_combination_set_item_start_index:
            # itemLine = fileLines[i]
            # item = int(itemLine[fileLines[i].find('[') + len('['):fileLines[i].find(']')])
            if fileLines[i+2].find('Binary string (Bin)') == -1:
                bcsList.append("")
        elif fileLines[i].find('Binary string (Bin) :') != -1:
                bcsLine = fileLines[i]
                bcs = bcsLine[fileLines[i].find('Binary string (Bin) :') + len(
                    'Binary string (Bin) : '):]
                bcsList.append(UtilsLib.convertBCS(bcs, False))
        elif fileLines[i].find('nonCriticalExtension') != -1:
            break
        i += 1


def parseHighOrderModulationTEMSFormat(lines):
    dicMod = {}
    found = False
    for i, modulation in enumerate(lines):
        if modulation.find("SupportedBandListEUTRA-v1250 :") != -1:
            found = True
        elif found and modulation.find("dl-256QAM-r12:") != -1:
            dicMod = {}
            modLine = lines[i]
            downlink = modLine[lines[i].find("dl-256QAM-r12") + len("dl-256QAM-r12: "):]
            dicMod['dl-256QAM-r12'] = downlink
        elif found and modulation.find("ul-64QAM-r12") != -1:
            modLine = lines[i]
            uplink = modLine[lines[i].find("ul-64QAM-r12") + len("ul-64QAM-r12: "):]
            dicMod['ul-64QAM-r12'] = uplink
            modulationList.append(dicMod)
        elif found and modulation.find("freqBandPriorityAdjustment") != -1:
            break
    # if there is no support for 256QAM or 64QAM
    if found == False:
        for band in enumerate(bandsList):
            dicMod = {}
            dicMod['dl-256QAM-r12'] = "not supported"
            dicMod['ul-64QAM-r12'] = "not supported"
            modulationList.append(dicMod)

    # BETA version: if found NR Band, just fill with Not Informed both UL and DL
    if UtilsLib.findstring(lines, "en-DC-r15: supported") is not None:
        bandlistSize = len(bandsList)
        modulationListSize = len(modulationList)
        diffSize = bandlistSize - modulationListSize
        if diffSize > 0:
            for i in range(diffSize):
                dicMod = {'dl-256QAM-r12': "not informed", 'ul-64QAM-r12': "not informed"}
                modulationList.append(dicMod)


# ************* Called from main loop. This method will call all other parsers *****************
def parseTEMSFormat(lines,fileName):
    # Parse supported LTE bands
    parseSupportedBandsTEMSFormat(lines)

    # Parse supported band combination
    parseBandCombinationTEMSFormat(lines)

    # Parse supported BCS
    parseBandwidthCombinationSetTEMSFormat(lines)

    # Parse support for 256QAM in DL and 64QAM in UL
    parseHighOrderModulationTEMSFormat(lines)

    # Write table on Excel
    ExcelHandler.write2Excel(bandsList, bandCombinationList, layersList, bcsList, modulationList, fileName)