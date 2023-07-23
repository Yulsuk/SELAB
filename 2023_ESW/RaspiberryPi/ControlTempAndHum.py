import DB#for sql

import Adafruit_DHT as dht#dht sensor lib

from datetime import datetime#for judgement day or night
import time

now = datetime.now()
DHT_GPIO = 4

class MesureTempAndHum:
    def __init__(self):
        self.temp = 0
        self.hum = 0
        
    def SetTempAndHum(self):
        self.hum, self.temp = dht.read_retry(dht.DHT22, DHT_GPIO) #mesure temp and hum
        self.hum = round(self.hum, 1)
        self.temp = round(self.temp, 1)
        
    def GetTempAndHum(self):
        return self.hum, self.temp
        
    def SendTempAndHumToDB(self):
        DB.SendTempAndHumToDB(self.temp, self.hum)

class JudgementTempAndHumControlFunction:
    def __init__(self):
        self.incTemp = False
        self.decTemp = False
        self.incHum = False
        self.decHum = False
        self.suitableTempMaxDay = 0.0
        self.suitableTempMinDay = 0.0
        self.suitableTempMaxNight = 0.0
        self.suitableTempMinNight = 0.0
        self.suitableHumMax = 0.0
        self.suitableHumMin = 0.0
        self.temp = 0.0
        self.hum = 0.0
    
    def SetSuitableTempAndHum(self):
        suitableTempAndHum = DB.ReadSuitableTempAndHum()#read suitable temp and hum from db
        garbage, self.suitableTempMaxDay, self.suitableTempMinDay, self.suitableTempMaxNight, self.suitableTempMinNight, self.suitableHumMax, self.suitableHumMin = suitableTempAndHum[0]#garbage is id
    
    def SetGreenHouseTemp(self, temp, hum):
        self.temp = temp
        self.hum = hum
    
    def SetTempAndHumIncOrDec(self):
        if range(6 <= now.hour <= 18):#if now is day
            print("Day")
            if self.suitableTempMinDay <= self.temp <= self.suitableTempMaxDay:
                self.incTemp, self.decTemp = False, False
                print("T Good")
            elif self.temp <= self.suitableTempMinDay:
                self.incTemp, self.decTemp = True, False
                print("T UP")
            elif self.suitableTempMaxDay <= self.temp:
                self.incTemp, self.decTemp = False, True
                print("T DOWN")
        else :
            if self.suitableTempMinNight <= self.temp <= self.suitableTempMaxNight: #if now is night
                self.incTemp, self.decTemp = False, False
                print("T Good")
            elif self.temp <= self.suitableTempMinNight:
                self.incTemp, self.decTemp = True, False
                print("T UP")
            elif self.suitableTempMaxNight <= self.temp:
                self.incTemp, self.decTemp = False, True
                print("T DOWN")
        
        if self.suitableHumMin <= self.hum <= self.suitableHumMax:
            self.incHum, self.decHum = False, False
            print("H Good")
        elif self.hum <= self.suitableHumMin:
            self.incHum, self.decHum = True, False
            print("H UP")
        elif self.suitableHumMax <= self.hum:
            self.incHum, self.decHum = False, True
            print("H DOWN")
                
    
    def GetTempAndHumIncOrDec(self):
        return self.incTemp, self.decTemp, self.incHum, self.decHum
        
        
        

        
if __name__ == '__main__':
    MesureTempAndHum = MesureTempAndHum()
    JudgementTempAndHumControlFunction = JudgementTempAndHumControlFunction()
    
    JudgementTempAndHumControlFunction.SetSuitableTempAndHum()
    JudgementTempAndHumControlFunction.SetGreenHouseTemp(50.0,90.0)
    JudgementTempAndHumControlFunction.SetTempAndHumIncOrDec()
    print(JudgementTempAndHumControlFunction.GetTempAndHumIncOrDec())   
    
    temp = 0
    hum = 0
    
    
    
    while True:
        MesureTempAndHum.SetTempAndHum()
        hum, temp = MesureTempAndHum.GetTempAndHum()
        MesureTempAndHum.SendTempAndHumToDB()
        print("Temp : ",temp,"Hum : ",hum)
        
