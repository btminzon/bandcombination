import WiresharkFormat
import QualcommFormat
import TEMSFormat

def readInformation(text, fileName, country=None, modelName=None):
    wiresharkFormat = False
    temsFormat = False
    checkNextLine = False
    for supportedBands in text:
        if supportedBands.find("supportedBandListEUTRA:") != -1:
            wiresharkFormat = True
            break
        elif checkNextLine:
            if supportedBands.find("SupportedBandListEUTRA :") != -1:
                temsFormat = True
                break
            else: # Qualcomm format was found
                wiresharkFormat = False
                break
        elif supportedBands.find("supportedBandListEUTRA") != -1:
            checkNextLine = True

    if wiresharkFormat:
        WiresharkFormat.parseWiresharkFormat(text, fileName)
    elif temsFormat:
        TEMSFormat.parseTEMSFormat(text, fileName)
    else:
        QualcommFormat.parseQualcommFormat(text, fileName)
