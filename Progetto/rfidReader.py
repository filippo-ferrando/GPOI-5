# https://pimylifeup.com/raspberry-pi-rfid-rc522/

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import datetime
import logging

LOGGING_FILE = f"log/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-log.log"

logging.basicConfig(filename=LOGGING_FILE, encoding='utf-8', level=logging.DEBUG)

class rfidReader():
    def __init__(self):
        reader = SimpleMFRC522()

    def read(self):
        try:
            mat = self.reader.read()
            return mat
            logging.debug("Begin reading...")
        except:
            logging.critical("Failed reading")
        finally:
            GPIO.cleanup()
            logging.debug("Finished reading...")

    def write(self):
        try:
            text = input('Inserisci i dati:')
            print("Posiziona il tag")
            self.reader.write(text)
            print("Scritto")
            logging.debug("Begin writing...")
        except:
            logging.critical("Failed writing")
        finally:
            GPIO.cleanup()
            logging.debug("Finished writing...")

    def stringCreator(self):
        logging.debug("String creation...")

        mat = self.read()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        string = f"{date},{mat}"
        print(f"{date} --> {mat}")


#           .--.          
# ::\`--._,'.::.`._.--'/::
# ::::.  ` __::__ '  .::::
# ::::::-:.`'..`'.:-::::::
# ::::::::\ `--' /::::::::
