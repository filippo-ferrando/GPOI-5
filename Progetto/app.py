import requests
from rfidReader import lettore
import threading as thr
from datetime import datetime

import RPi.GPIO as GPIO
from gpiozero import Buzzer

global offsetTagDict
offsetTagDict = {}

class tagController(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        global offsetTagList
        while self.runnning:
            for element in offsetTagDict.values():
                if (datetime.now().strftime('%H:%M:%S') - element) >= 30:
                    wKey = list(offsetTagDict.keys())[list(offsetTagDict.values()).index(element)]
                    offsetTagDict.pop(wKey)



class raspberry(self):
    def __init__(self):
        self.api = "https://testgpoi2022.netsons.org/pres_auto/config/PHP/api_controllo_timbr.php"
        self.password = "Rasp_rfid"
        self.Rled = 18
        self.Gled = 22
        self.buzzer = Buzzer(26)

    def reader(self):
        uid = lettore.readT()
        if uid in offsetTagDict.keys():
            uid = 403
        else:
            offsetTagDict["uid"] = uid
            return uid

    def send(self, uid):
        if uid == 403:
            self.repeated_tag()
        else:
            http = requests.post(self.api,data={'codMatr' : uid, 'password' : self.password})
            return http.text

    def bip(self, resp):
        if resp == "si":
            GPIO.output(self.Gled, HIGH)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            time.sleep(0.3)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            GPIO.output(self.Gled, LOW)
        elif resp == "no":
            GPIO.output(self.Rled, HIGH)
            self.buzzer.on()
            time.sleep(1)
            self.buzzer.off()
            GPIO.output(self.Rled, LOW)


    def repeated_tag(self):
        GPIO.output(self.Rled, HIGH)
        time.sleep(1)
        GPIO.output(self.Rled, LOW)
        
        
