import requests
import threading as thr
from datetime import datetime
import time
import urllib.request
import os
import logging

from pirc522 import RFID
import RPi.GPIO as GPIO
from gpiozero import Buzzer

#global offsetTagDict
#offsetTagDict = {}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# LOGGING PLATFORM
LOGGING_FILE = "./log/log.log"
logging.basicConfig(filename=LOGGING_FILE, encoding="utf-8", level=logging.DEBUG)

pid = os.getpid()
f = open("pid.txt", "w")
f.write(f"{pid}")
f.close()

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

'''
class tagController(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self)
        self.running = True

    def run(self):
        global offsetTagList
        while self.running:
            for element in offsetTagDict.values():
                if int((time.time() - element)) >= 30:
                    wKey = list(offsetTagDict.keys())[list(offsetTagDict.values()).index(element)]
                    offsetTagDict.pop(wKey)
'''

class raspberry():
    def __init__(self):
        self.api = "https://testgpoi2022.netsons.org/pres_auto/config/codice/api_controllo_timbr.php"
        self.password = "Rasp_rfid"
        self.Rled = 11
        GPIO.setup(self.Rled,GPIO.OUT)
        self.Gled = 13
        GPIO.setup(self.Gled,GPIO.OUT)
        self.buzzer = Buzzer(26)
        self.rc522 = RFID()

        if connect():
            logging.debug(f"Connected to internet")
        else:
            logging.critical(f"Not connected")
            os._exit(0)

    def reader(self):
        #global offsetTagDict

        try:

            print('Waiting for the badge: ')

            self.rc522.wait_for_tag()
            (error, tag_type) = self.rc522.request()

            if not error : 
                (error, uid) = self.rc522.anticoll()

                if not error :
                    uid = "".join(str(l) for l in uid)
                    print(f'badge : {uid}')
                    time.sleep(0.5)

                    return uid
        except KeyboardInterrupt:
            print("chiusura")
        '''
        if uid in offsetTagDict:
            uid = 403
        else:
            offsetTagDict[uid] = time.time()
            return uid
        '''

        

    def send(self, uid):
        '''
        if uid == 403:
            self.repeated_tag()
        else:
            http = requests.post(self.api,data={'uid' : uid, 'password' : self.password, 'modalita' : "modalita"})
            return http.text
        '''
        if connect():
            logging.debug(f"Connected to internet")
        else:
            logging.critical(f"Not connected - Cannot send info")
            os._exit(0)

        http = requests.post(self.api,data={'uid' : uid, 'password' : self.password, 'modalita' : "modalita"})
        logging.debug(f"{datetime.now()} - UID {uid} Sended")
        return http.text


    def bip(self, resp):
        if resp == "si":
            logging.debug(f"{datetime.now()} - Positive Response")
            GPIO.output(self.Gled, GPIO.HIGH)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            time.sleep(0.3)
            self.buzzer.on()
            time.sleep(0.3)
            self.buzzer.off()
            GPIO.output(self.Gled, GPIO.LOW)
        elif resp == "no":
            logging.debug(f"{datetime.now()} - Negative Response")
            GPIO.output(self.Rled, GPIO.HIGH)
            self.buzzer.on()
            time.sleep(1)
            self.buzzer.off()
            GPIO.output(self.Rled, GPIO.LOW)
        elif resp == "password":
            logging.debug(f"{datetime.now()} - 500 : Internal server error ")
            print("PASSWORD SBAGLIATA")

    '''
    def repeated_tag(self):
        GPIO.output(self.Rled, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.Rled, GPIO.LOW)
    '''    
        
rasp = raspberry()

#controlList = tagController()
#controlList.start()
time.sleep(0.5)
if not connect():
    print("Not connected to internet, exiting...")
    logging.critical(f"{datetime.now()} - Failed to connect to internet")
    #os.sys.exit()
else:
    print("connected")
    logging.debug(f"{datetime.now()} - Connected to internet")

while True:
    time.sleep(3)
    uid = rasp.reader()
    resp = rasp.send(uid)
    rasp.bip(resp)