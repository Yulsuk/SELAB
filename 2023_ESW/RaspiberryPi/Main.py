import ControlTempAndHum
import SnowRemoval
import MicrodustRemoval
import DetectInvader

import time


if __name__ == '__main__':
    #1. Object declare
    MesureTempAndHum = ControlTempAndHum.MesureTempAndHum()
    
    
    #2. Variable declare
    temp = 0
    hum = 0
    automatic = False

    #Object detected with camera : String
    #Wiper, Greenhouse Side, Waterspray inside, Ventilator, Heating wire : boolean
    #Waterspray outside : boolean
    
    #3. while
    while True:
        #4. Mesure temp and hum
        MesureTempAndHum.SetTempAndHum()
        hum, temp = MesureTempAndHum.GetTempAndHum()
        #5. Mesure pressure
        print("Temp : ", temp,"Hum : ", hum)
        #6. MicroDUst?
        #7. Camera?
        
        #8. if
            #7. if automatic
                #Read suitalbe Temp and Hum from DB
                #Set greenhouse temp and hum in Judgement class
                #
            #8. if manual
                #update every operate value

