import RPi.GPIO as GPIO 
from pirc522 import RFID
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class lettore():
    def __init__(self):
        self.rc522 = RFID()

    def readT(self):
        print('In attesa del badge (per quittare, Ctrl + c): ')
        rc522.wait_for_tag()
        (error, tag_type) = rc522.request()

        if not error : 
            (error, uid) = rc522.anticoll()

            if not error :
                print('Uid del badge : {}'.format(uid))
                return uid
                time.sleep(1)

#           .--.          
# ::\`--._,'.::.`._.--'/::
# ::::.  ` __::__ '  .::::
# ::::::-:.`'..`'.:-::::::
# ::::::::\ `--' /::::::::
