import os
import psutil
import time

logging.basicConfig(filename="/home/pi/GPOI-5/Progetto/log/pid-log.log", encoding="utf-8", level=logging.DEBUG)


while True:
    
    try:
        with open("/home/pi/GPOI-5/Progetto/pid.txt") as f:
            lines = f.readlines()
            logging.debug(f"PID = {lines[0]}") #PID from the main process
            for proc in psutil.process_iter():
                try:
                    if lines[0] == proc.pid:
                        print("Process exist - Doing nothing")
                    else:
                        os.system("python3 app.py")
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
    except FileNotFoundError:
        print("File not found")

    time.sleep(300)



