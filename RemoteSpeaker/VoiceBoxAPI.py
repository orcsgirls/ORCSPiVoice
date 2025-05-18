import json
import os
import subprocess
import tempfile
import glob
import socket
from os import path, getuid
from flask import Flask, request, jsonify, render_template
from aiy.voice.audio import play_wav
from aiy.leds import Leds, Color

SOUND_FOLDER = os.path.split(os.path.abspath(__file__))[0]+"/sounds/"
sounds = glob.glob(path.join(SOUND_FOLDER,'*.wav'))

app = Flask(__name__)
leds = Leds()


#--- Helpers ----------------------------------------------------

RUN_DIR = '/run/user/%d' % getuid()

def say(text, lang='en-GB', pitch=130, speed=100, device='default'):
    data = "<pitch level='%d'><speed level='%d'>%s</speed></pitch>" % \
           (pitch, speed, text)
    
    with tempfile.NamedTemporaryFile(suffix='.wav', dir=RUN_DIR) as f:
        cmd = 'pico2wave --wave %s --lang %s "%s" && aplay -q -D %s %s' % \
             (f.name, lang, data, device, f.name)
        subprocess.check_call(cmd, shell=True)

def set_volume(volume_level):
    command = ["amixer", "--card", "0", "sset", "Speaker", f"{volume_level}%"]
    subprocess.run(command, stdout = subprocess.DEVNULL)

set_volume(50)

#--- Helper page ------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html', host=socket.gethostname())

#--- PLay sound file --------------------------------------------

@app.route('/play', methods=['GET'])
def play_sound():
    value = request.args.get('value')
    file = path.join(SOUND_FOLDER,value+'.wav')
    if path.exists(file):
        play_wav(file)
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'sound not found'})

#--- Control button led -----------------------------------------

@app.route('/led', methods=['GET'])
def control_led():
    value = request.args.get('value')
    if value == 'red':
        leds.update(Leds.rgb_on(Color.RED))
    elif value == 'green':
        leds.update(Leds.rgb_on(Color.GREEN))
    elif value == 'blue':
        leds.update(Leds.rgb_on(Color.BLUE))
    elif value == 'cyan':
        leds.update(Leds.rgb_on(Color.CYAN))
    elif value == 'purple':
        leds.update(Leds.rgb_on(Color.PURPLE))
    elif value == 'white':
        leds.update(Leds.rgb_on(Color.WHITE))
    elif value == 'yellow':
        leds.update(Leds.rgb_on(Color.YELLOW))
    elif value == 'off':
        leds.update(Leds.rgb_off())
    else:
        return jsonify({'status': 'invalid color'})
        
    return jsonify({'status': 'ok'})

#--- Set volume --------------------------------------------------

@app.route('/volume', methods=['GET'])
def volume():
    value = request.args.get('value')
    if(value):
        set_volume(int(value))
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'error': 'missing parameter'})

#--- Say given text ----------------------------------------------

@app.route('/say', methods=['GET'])
def do_speak():
    pitch = request.args.get('pitch') if request.args.get('pitch') else 130
    value = request.args.get('value')
    if(value):
        say(value, pitch=int(pitch))
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'error': 'missing text'})

#--- List available sound files ----------------------------------

@app.route('/list', methods=['GET'])
def list_sounds():
    if(len(sounds)>0):
        return jsonify([{'sound': os.path.basename(s)} for s in sounds])
    else:
        return jsonify({'error': 'no sounds found'})
    
#--------------------------------------------------------------

app.run(host='0.0.0.0', port=5000)
