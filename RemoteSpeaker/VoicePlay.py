#!/usr/bin/python3

import requests
import time
from urllib.parse import quote

# The URL to the Voicebox you want to control
VOICE_URL = "http://10.0.0.126:5000"  # Note https does not work the way we are set up

# Example to change the Led color
response = requests.get(VOICE_URL+'/led?value=green')

# Example to play sound
response = requests.get(VOICE_URL+'/play?value=Boing&volume=40')

# Example to speak some text. Note the quote command takes care of proper encoding for a link
text = quote("ORCSGirls are the best")
response = requests.get(VOICE_URL+'/say?value='+text)

# Simple loop to blink the Led in differnt colors
colors=['red','green','blue']
for c in colors:
    response = requests.get(VOICE_URL+'/led?value='+c)
    time.sleep(1.0)

# Turning Led back off
response = requests.get(VOICE_URL+'/led?value=off')

