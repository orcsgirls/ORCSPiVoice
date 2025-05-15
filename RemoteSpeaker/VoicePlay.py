#!/usr/bin/python3

import requests
import time
from urllib.parse import quote

import subprocess

def set_volume(volume_level):
    """Sets the ALSA volume level.

    Args:
        volume_level: An integer between 0 and 100 representing the desired volume percentage.
    """
    command = ["amixer", "sset", "Master", f"{volume_level}%"]
    subprocess.run(command, stdout = subprocess.DEVNULL)


VOICE_URL = "http://10.0.0.126:5000"  # Note https does not work the way we are set up
response = requests.get(VOICE_URL+'/led?value=green')

for i in range(10):
    response = requests.get(VOICE_URL+'/led?value=green')
    time.sleep(0.1)
    response = requests.get(VOICE_URL+'/led?value=off')
    time.sleep(0.1)
    response = requests.get(VOICE_URL+'/play?value=boing&volume='+str(i*7))

text = "ORCSGirls are the best"
value = quote(text)
print(value)
response = requests.get(VOICE_URL+'/say?value='+value)
print(response.json())
