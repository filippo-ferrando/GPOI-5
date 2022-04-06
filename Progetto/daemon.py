import os
import psutil
import time

while True:
    time.sleep(300)
    try:
        with open("./pid.txt") as f:
            lines = f.readlines()
            print(lines[0]) #PID from the main process
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



