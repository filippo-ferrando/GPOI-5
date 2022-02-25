#! /bin/bash

sudo apt install figlet > log/install-log.log 2>&1

echo "First install" | figlet

sudo apt update >> log/install-log.log 2>&1
sudo apt upgrade >> log/install-log.log 2>&1
sudo apt install python3 python3-pip  >> log/install-log.log 2>&1
pip3 install -r requirements.txt > log/install-log.log 2>&1