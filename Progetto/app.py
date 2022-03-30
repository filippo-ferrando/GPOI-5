import requests
import threading as thr
from datetime import datetime
import time
import urllib.request
import os

from pirc522 import RFID
import RPi.GPIO as GPIO
from gpiozero import Buzzer

global offsetTagDict
offsetTagDict = {}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


class tagController(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        global offsetTagList
        while self.running:
            for element in offsetTagDict.values():
                if (datetime.now().strftime('%H:%M:%S') - element) >= 30:
                    wKey = list(offsetTagDict.keys())[list(offsetTagDict.values()).index(element)]
                    offsetTagDict.pop(wKey)


class raspberry():
    def __init__(self):
        self.api = "https://testgpoi2022.netsons.org/pres_auto/config/codice/api_controllo_timbr.php"
        self.password = "Rasp_rfid"
        self.Rled = 12
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.Rled,GPIO.OUT)
        self.Gled = 7
        GPIO.setup(self.Gled,GPIO.OUT)
        self.buzzer = Buzzer(26)
        self.rc522 = RFID()
        if not connect():
            print("Not connected to internet, exiting...")
            os.sys.exit()

    def reader(self):
        global offsetTagDict
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        print('In attesa del badge (per quittare, Ctrl + c): ')

        self.rc522.wait_for_tag()
        (error, tag_type) = self.rc522.request()

        if not error : 
            (error, uid) = self.rc522.anticoll()

            if not error :
                print('Uid del badge : {}'.format(uid))
                uid = str(uid)
                time.sleep(0.5)

        if uid in offsetTagDict.keys():
            uid = 403
        else:
            offsetTagDict["uid"] = uid
            return uid

    def send(self, uid):
        if uid == 403:
            self.repeated_tag()
        else:
            http = requests.post(self.api,data={'codMatr' : uid, 'password' : self.password, 'modalita' : "modalita"})
            return http.text

    def bip(self, resp):
        if resp == "si":
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.output(self.Gled, GPIO.HIGH)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            self.buzzer.on()
            time.sleep(0.3)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            self.buzzer.off()
            time.sleep(0.3)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.output(self.Gled, GPIO.LOW)
        elif resp == "no":
            GPIO.setmode(GPIO.BCM)
            GPIO.output(self.Rled, GPIO.HIGH)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            self.buzzer.on()
            time.sleep(1)
            self.buzzer.off()
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.output(self.Rled, GPIO.LOW)
        elif resp == "password":
            print("PASSWORD SBAGLIATA")


    def repeated_tag(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.output(self.Rled, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.Rled, GPIO.LOW)
        
        
rasp = raspberry()

controlList = tagController()
controlList.start()

while True:
    uid = rasp.reader()
    resp = rasp.send(uid)
    rasp.bip(resp)