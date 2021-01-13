import WiresharkFormat
import QualcommFormat
import TEMSFormat

def readInformation(text, fileName):
    wiresharkFormat = False
    temsFormat = False
    checkNextLine = False
    for supportedBands in text:
        if supportedBands.find("ue-CapabilityRAT-ContainerList:") != -1:
            wiresharkFormat = True
            break
        elif supportedBands.find("UE-CapabilityRAT-ContainerList") != -1:
            temsFormat = True
            break

    if wiresharkFormat:
        WiresharkFormat.parseWiresharkFormat(text, fileName)
    elif temsFormat:
        TEMSFormat.parseTEMSFormat(text, fileName)
    else:
        QualcommFormat.parseQualcommFormat(text, fileName)
