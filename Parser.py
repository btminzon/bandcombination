import WiresharkFormat
import QualcommFormat

def readInformation(text, fileName, country=None, modelName=None):
    wiresharkFormat = False
    for supportedBands in text:
        if supportedBands.find("supportedBandListEUTRA :") != -1:
            wiresharkFormat = True
            break
        elif supportedBands.find("supportedBandListEUTRA") != -1:
            wiresharkFormat = False
            break
    if wiresharkFormat:
        WiresharkFormat.parseWiresharkFormat(text,fileName,country,modelName)
    else:
        QualcommFormat.parseQualcommFormat(text,fileName,country,modelName)