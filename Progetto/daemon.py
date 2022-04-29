import os
import psutil
import time
from datetime import datetime
import logging

logging.basicConfig(filename="/home/pi/log/pid-log.log", encoding="utf-8", level=logging.DEBUG)


while True:
    
    try:
        with open("/home/pi/pid.txt") as f:
            lines = f.readlines()
            logging.debug(f"PID = {lines[0]}") #PID from the main process
            for proc in psutil.process_iter():
                try:
                    if lines[0] == proc.pid:
                        #print("Process exist - Doing nothing")
                        logging.debug(f"{datetime.now()} - Process exist, doing nothing")
                    else:
                        logging.debug(f"{datetime.now()} - Process dead, starting")
                        os.system("python3 app.py")
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
    except FileNotFoundError:
        logging.critical(f"{datetime.now()} - File not found")
        #print("File not found")

    time.sleep(20)



