import DB#for sql
from PIN import *
import Adafruit_DHT as dht#dht sensor lib

from datetime import datetime#for judgement day or night
import time

#pi = pigpio.pi()

class MesureTempAndHum:
    def __init__(self):
        self.temp = 0
        self.hum = 0
        
    def SetTempAndHum(self):
        #self.hum, self.temp = dht.read_retry(dht.DHT22, DHT_GPIO) #mesure temp and hum
        #self.hum = round(self.hum, 1)
        #self.temp = round(self.temp, 1)
        self.hum = 40
        self.temp = 20
        
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
        controlValue = DB.ReadControlValue()
        controlValue = controlValue[0][0]
        if controlValue == 1:#oh lee
            print("Selected Corps : cucumber")
            self.suitableTempMaxDay = 28.0
            self.suitableTempMinDay = 22.0
            self.suitableTempMaxNight = 18.0
            self.suitableTempMinNight = 15.0
            self.suitableHumMax = 80.0
            self.suitableHumMin = 60.0
        elif controlValue == 2:#tomato
            print("Selected Corps : tomato")
            self.suitableTempMaxDay = 26.0
            self.suitableTempMinDay = 24.0
            self.suitableTempMaxNight = 17.0
            self.suitableTempMinNight = 13.0
            self.suitableHumMax = 80.0
            self.suitableHumMin = 70.0
        elif controlValue == 3:#strewberry?
            print("Selected Corps : strewberry")
            self.suitableTempMaxDay = 25.0
            self.suitableTempMinDay = 18.0
            self.suitableTempMaxNight = 15.0
            self.suitableTempMinNight = 11.0
            self.suitableHumMax = 80.0
            self.suitableHumMin = 70.0
    
    def SetGreenHouseTemp(self, temp, hum):#set require in main
        self.temp = temp
        self.hum = hum
    
    def SetTempAndHumIncOrDec(self):
        self.now = datetime.now()
        if range(6 <= self.now.hour <= 18):#if now is day
            print("Now is Day")
            if self.suitableTempMinDay <= self.temp <= self.suitableTempMaxDay:#if temp suitalbe : do nothing
                self.incTemp, self.decTemp = False, False
            elif self.temp <= self.suitableTempMinDay:                          #if temp is low : incTemp = True
                self.incTemp, self.decTemp = True, False
            elif self.suitableTempMaxDay <= self.temp:                          #if temp is high : decTemp = True
                self.incTemp, self.decTemp = False, True
        else :
            print("Now is Night")
            if self.suitableTempMinNight <= self.temp <= self.suitableTempMaxNight: #if now is night
                self.incTemp, self.decTemp = False, False
            elif self.temp <= self.suitableTempMinNight:
                self.incTemp, self.decTemp = True, False
            elif self.suitableTempMaxNight <= self.temp:
                self.incTemp, self.decTemp = False, True
        
        if self.suitableHumMin <= self.hum <= self.suitableHumMax:#about humidity
            self.incHum, self.decHum = False, False
        elif self.hum <= self.suitableHumMin:
            self.incHum, self.decHum = True, False
        elif self.suitableHumMax <= self.hum:
            self.incHum, self.decHum = False, True
    
    def GetTempAndHumIncOrDec(self):
        return self.incTemp, self.decTemp, self.incHum, self.decHum
        
class ControlInsideWaterSpray:
    def __init__(self):
        self.operateInsideWaterSprayer = False
    
    def SetJudgementOperateInsideSpray(self, incTemp, decTemp, incHum, decHum):
        if(incTemp == False and decTemp == False and incHum == False and decHum == False):
            self.operateInsideWaterSprayer = False
        elif(incTemp == False and decTemp == False and incHum == True and decHum == False):
            self.operateInsideWaterSprayer = True
        elif(incTemp == False and decTemp == False and incHum == False and decHum == True):
            self.operateInsideWaterSprayer = False
        elif(incTemp == True and decTemp == False and incHum == False and decHum == False):
            self.operateInsideWaterSprayer = False
        elif(incTemp == False and decTemp == True and incHum == False and decHum == False):
            self.operateInsideWaterSprayer = True
        elif(incTemp == True and decTemp == False and incHum == True and decHum == False):
            self.operateInsideWaterSprayer = False
        elif(incTemp == True and decTemp == False and incHum == False and decHum == True):
            self.operateInsideWaterSprayer = False
        elif(incTemp == False and decTemp == True and incHum == True and decHum == False):
            self.operateInsideWaterSprayer = True
        elif(incTemp == False and decTemp == True and incHum == False and decHum == True):
            self.operateInsideWaterSprayer = True
            
    
    def SetOperateInsideWaterSpray(self):
        if self.operateInsideWaterSprayer == True:
            GPIO.output(INSIDE_WATERSPRAY,True)
            print('spray is operating')
        else:
            GPIO.output(INSIDE_WATERSPRAY,False)
            print('spray is idle')

class ControlGreenHouseSide:
    def __init__(self):
        self.openGreenHouseSide = False
        self.closeGreenHouseSide = False
    
    def SetJudgementOperateGreenhouseSide(self, incTemp, decTemp, incHum, decHum):
        if(incTemp == False and decTemp == False and incHum == False and decHum == False):
            self.openGreenHouseSide = False
            self.closeGreenHouseSide = False
        elif(incTemp == False and decTemp == False and incHum == True and decHum == False):
            self.openGreenHouseSide = False
            self.closeGreenHouseSide = True
        elif(incTemp == False and decTemp == False and incHum == False and decHum == True):
            self.openGreenHouseSide = True
            self.closeGreenHouseSide = False
        elif(incTemp == True and decTemp == False and incHum == False and decHum == False):
            self.openGreenHouseSide = False
            self.closeGreenHouseSide = True
        elif(incTemp == False and decTemp == True and incHum == False and decHum == False):
            self.openGreenHouseSide = True
            self.closeGreenHouseSide = False
        elif(incTemp == True and decTemp == False and incHum == True and decHum == False):
            self.openGreenHouseSide = False
            self.closeGreenHouseSide = True
        elif(incTemp == True and decTemp == False and incHum == False and decHum == True):
            self.openGreenHouseSide = False
            self.closeGreenHouseSide = True
        elif(incTemp == False and decTemp == True and incHum == True and decHum == False):
            self.openGreenHouseSide = True
            self.closeGreenHouseSide = False
        elif(incTemp == False and decTemp == True and incHum == False and decHum == True):
            self.openGreenHouseSide = True
            self.closeGreenHouseSide = False
    
    def SetOperateGreenHouseSide(self):
        if self.openGreenHouseSide == True and self.closeGreenHouseSide == False:
            pi.set_servo_pulsewidth(SERVO_MOTOR1,0)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,0)
            time.sleep(1)
            pi.set_servo_pulsewidth(SERVO_MOTOR1,500)  
            pi.set_servo_pulsewidth(SERVO_MOTOR2,2500)
            time.sleep(5)
            pi.set_servo_pulsewidth(SERVO_MOTOR1,0)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,0)
            print('green house side opening')
        elif self.closeGreenHouseSide == True and self.openGreenHouseSide == False:
            pi.set_servo_pulsewidth(SERVO_MOTOR1,0)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,0)
            time.sleep(1)
            pi.set_servo_pulsewidth(SERVO_MOTOR1,2500)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,500)  
            time.sleep(5)
            pi.set_servo_pulsewidth(SERVO_MOTOR1,0)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,0)
            print('green house side closing')
        else:
            pi.set_servo_pulsewidth(SERVO_MOTOR1,0)
            pi.set_servo_pulsewidth(SERVO_MOTOR2,0)
            print('green house side is idle')

class ControlVentilator:
    def __init__(self):
        self.operateVentilator = False
    
    def SetJudgementOperateVentilator(self, incTemp, decTemp, incHum, decHum):
        if(incTemp == False and decTemp == False and incHum == False and decHum == False):
            self.operateVentilator = False
        elif(incTemp == False and decTemp == False and incHum == True and decHum == False):
            self.operateVentilator = False
        elif(incTemp == False and decTemp == False and incHum == False and decHum == True):
            self.operateVentilator = True
        elif(incTemp == True and decTemp == False and incHum == False and decHum == False):
            self.operateVentilator = False
        elif(incTemp == False and decTemp == True and incHum == False and decHum == False):
            self.operateVentilator = True
        elif(incTemp == True and decTemp == False and incHum == True and decHum == False):
            self.operateVentilator = False
        elif(incTemp == True and decTemp == False and incHum == False and decHum == True):
            self.operateVentilator = False
        elif(incTemp == False and decTemp == True and incHum == True and decHum == False):
            self.operateVentilator = True
        elif(incTemp == False and decTemp == True and incHum == False and decHum == True):
            self.operateVentilator = True
    
    def SetOperateVentilator(self):
        if self.operateVentilator == True:
            GPIO.output(FAN,True)
            print('ventilator is operating')
        else:
            GPIO.output(FAN,False)
            print('ventilator is idle')
            
class ControlHeatingWire:
    def __init__(self):
        self.operateHeatingWire = False
    
    def SetJudgementOperateHeatingWire(self, incTemp, decTemp, incHum, decHum):
        if(incTemp == False and decTemp == False and incHum == False and decHum == False):
            self.operateHeatingWire = False
        elif(incTemp == False and decTemp == False and incHum == True and decHum == False):
            self.operateHeatingWire = False
        elif(incTemp == False and decTemp == False and incHum == False and decHum == True):
            self.operateHeatingWire = False
        elif(incTemp == True and decTemp == False and incHum == False and decHum == False):
            self.operateHeatingWire = True
        elif(incTemp == False and decTemp == True and incHum == False and decHum == False):
            self.operateHeatingWire = False
        elif(incTemp == True and decTemp == False and incHum == True and decHum == False):
            self.operateHeatingWire = True
        elif(incTemp == True and decTemp == False and incHum == False and decHum == True):
            self.operateHeatingWire = True
        elif(incTemp == False and decTemp == True and incHum == True and decHum == False):
            self.operateHeatingWire = False
        elif(incTemp == False and decTemp == True and incHum == False and decHum == True):
            self.operateHeatingWire = False
    
    def SetOperateHeatingWire(self):
        if self.operateHeatingWire == True:
            print('heatingWire is operating')
        else:
            print('heatingWire is idle')
        
        
        
        

        
if __name__ == '__main__':
    MesureTempAndHum = MesureTempAndHum()
    JudgementTempAndHumControlFunction = JudgementTempAndHumControlFunction()
    ControlInsideWaterSpray = ControlInsideWaterSpray()
    ControlGreenHouseSide = ControlGreenHouseSide()
    ControlHeatingWire = ControlHeatingWire()
    ControlVentilator = ControlVentilator()
    
    tem = 0
    hum = 0
    incTemp = False
    decTemp = False
    incHum = False
    decHum = False
    
    while True:
        MesureTempAndHum.SetTempAndHum()
        hum, temp = MesureTempAndHum.GetTempAndHum()
        #MesureTempAndHum.SendTempAndHumToDB()
        print("Green House Temp And Hum : ",temp, hum)
        JudgementTempAndHumControlFunction.SetSuitableTempAndHum()
        print("Suitable Temp and Hum", JudgementTempAndHumControlFunction.suitableTempMaxDay, JudgementTempAndHumControlFunction.suitableTempMinDay, JudgementTempAndHumControlFunction.suitableHumMax, JudgementTempAndHumControlFunction.suitableHumMin)
        
        JudgementTempAndHumControlFunction.SetGreenHouseTemp(temp,hum)
        JudgementTempAndHumControlFunction.SetTempAndHumIncOrDec()
        incTemp, decTemp, incHum, decHum = JudgementTempAndHumControlFunction.GetTempAndHumIncOrDec()
        print("TempAndHumIncOrDec : ",incTemp, decTemp, incHum, decHum)
        print("-----------------------Actuator-----------------------")
        ControlInsideWaterSpray.SetJudgementOperateInsideSpray(incTemp, decTemp, incHum, decHum)
        ControlInsideWaterSpray.SetOperateInsideWaterSpray()
        ControlGreenHouseSide.SetJudgementOperateGreenhouseSide(incTemp, decTemp, incHum, decHum)
        ControlGreenHouseSide.SetOperateGreenHouseSide()
        ControlHeatingWire.SetJudgementOperateHeatingWire(incTemp, decTemp, incHum, decHum)
        ControlHeatingWire.SetOperateHeatingWire()
        ControlVentilator.SetJudgementOperateVentilator(incTemp, decTemp, incHum, decHum)
        ControlVentilator.SetOperateVentilator()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
        time.sleep(5)
        
        
        
        
        
