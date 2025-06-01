#!/bin/sh

apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
python3.10 --version
apt install python3-pip -y
apt install python3.10-venv -y
apt install libgl1 -y

git clone https://github.com/X0re4ik/UrFU-Drone-Detection-Stream-Server.git
cd UrFU-Drone-Detection-Stream-Server
python3.10 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --no-root