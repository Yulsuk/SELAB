import spidev
import time
import RPi.GPIO as GPIO
Vcc = 5.0
R1 = 1000

spi = spidev.SpiDev()
spi.open(0, 0)
mcp3008_channel = 0
delay = 0.1

servo_pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

def ReadChannel(channel):
    adc = spi.xfer([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

class MesurePressure:
    def __init__(self):
        self.pressure = 0
    def SetPressure(self):
        analog_level = ReadChannel(mcp3008_channel)
        self.pressure = analog_level
    def GetPressure(self):
        return self.pressure

class JudgementCollapseRisk:
    def __init__(self):
        self.collapseRisk = False
        self.pressure = 0
    def SetPressure(self, pressure):
        self.pressure = pressure
    def SetCollapseRisk(self):
        if(self.pressure > 100):
            print("pressure : ",self.pressure)
            self.collapseRisk = True
        else:
            self.collapseRisk = False
    def GetCollapseRisk(self):
        return self.collapseRisk
        
class OperateSnowRemovalDevice:
    def __init__(self):
        self.operateSnowRemovalDevice = False
    def SetOperateSnowRemovalDevice(self, collapserisk):
        if(collapserisk == True):
            pwm.ChangeDutyCycle(4)
            time.sleep(1.0)
            pwm.ChangeDutyCycle(10)
            time.sleep(1.0)
        elif(collapserisk == False):
            pass
	
if __name__ == '__main__':
    MesurePressure = MesurePressure()
    JudgementCollapseRisk = JudgementCollapseRisk()
    OperateSnowRemovalDevice = OperateSnowRemovalDevice()
           
    pressure = 0
    collapserisk = False
    while True:
        MesurePressure.SetPressure()
        pressure = MesurePressure.GetPressure()
        JudgementCollapseRisk.SetPressure(pressure)
        JudgementCollapseRisk.SetCollapseRisk()
        collapserisk = JudgementCollapseRisk.GetCollapseRisk()
        OperateSnowRemovalDevice.SetOperateSnowRemovalDevice(collapserisk)
