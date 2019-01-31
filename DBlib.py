import pymysql
from os import getenv

########################
#Tables:
#   BAND_MODULATION
#   Colums:
#    *  COUNTRY
#    *  MODEL
#    *  BAND
#       256QAM
#       64QAM
#   BAND_COMBINATION
#   Columns
#    *  COUNTRY
#    *  MODEL
#    *  COMBO
#       BCS
#########################

BAND_MODULATION = "BAND_MODULATION"
BAND_COMBINATION = "BAND_COMBINATION"

class DBlib:
    def __init__(self, dbFolder = None):
        self.connectToSql()
        self.SupportedBands = 'BAND_MODULATION'
        self.BandCombination = 'BAND_COMBINATION'

    def connectToSql(self):
        try:
            self.con = pymysql.connect(host="192.168.0.5", user='admin', passwd='admin', db="Capability")
            self.cur = self.con.cursor()
            self.connected = True
            return True
        except:
            self.connected = False
            return False

    def get(self, table, model, country):
        if self.connected:
            query = "SELECT * FROM "+ table + " WHERE MODEL ='" + model + "' AND COUNTRY = '" + country
            self.cur.execute(query)
            if self.cur.rowcount > 0:
                return self.cur.fetchone()
        return None

    def save(self, table, country, model, band, qam256, qam64, combo, bcs):
        if self.connected:
            query = "SELECT * FROM " + table
            self.cur.execute(query)
            #if self.cur.rowcount == 0:
            if table == "BAND_COMBINATION":
                query = "INSERT INTO BAND_COMBINATION" + " (`COUNTRY`, `MODEL`, `COMBO`, `BCS`) VALUES ('" + country + "','" + model + "','" + combo + "','" + bcs + "')"
            elif table == "BAND_MODULATION":
                query = "INSERT INTO BAND_MODULATION" + " (`COUNTRY`, `MODEL`, `BAND`, `QAM256`, `QAM64`) VALUES ('" + country + "','" + model + "','" + band + "','" + qam256 + "','" + qam64 + "')"
            self.cur.execute(query)
            self.con.commit()

    def getModel(self, model):
        bandComb = self.get(self.SupportedBands,model)
        bandMod = self.get(self.BandCombination,model)
        return [bandComb[:],bandMod[:]]

def saveBandModulation(country, model, band, qam256, qam64):
    lib = DBlib()
    lib.save(BAND_MODULATION , country, model, band, qam256, qam64, None, None)

def saveBandCombination(country, model, combo, bcs):
    lib = DBlib()
    lib.save(BAND_COMBINATION, country, model, None, None, None, combo, bcs)
