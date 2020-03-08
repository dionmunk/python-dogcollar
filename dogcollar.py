from flask import Flask
import RPi.GPIO as GPIO
import json, time

# port to run the server on
serverport = 8080

# duration of beep/vibrate/static in seconds
duration = 5

# class to store switch name, pin, and state
class Switch:
    def __init__(self, name, pin, state):
        self.name = name
        self.pin = pin
        self.state = state

    # return switch name
    def name(self):
        return self.name

    # set switch to ON
    def on(self):
        GPIO.output(self.pin, 0)
        self.state = "1"
        # duration added so switch can only be on for a short period
        time.sleep(duration)
        GPIO.output(self.pin, 1)
        self.state = "0"

    # set switch to OFF
    def off(self):
        GPIO.output(self.pin, 1)
        self.state = "0"

    # toggle switch
    def toggle(self):
        if self.state == "1":
            self.off()
        elif self.state == "0":
            self.on()
    
    # return switch state
    def status(self):
        return self.state

# sets the RPi lib to use the broadcom pin mappings
GPIO.setmode(GPIO.BCM)

# turn off warnings that may come up with GPIO
GPIO.setwarnings(False)

# import config file
with open('config.json') as f:
    config = json.load(f)

# create list of Switches
switches = []
i = 0
for switch in config["switches"]:
    switches.insert(i, Switch(switch["name"], switch["pin"], "0"))
    i += 1

# set up GPIO pins that will be used for each Switch
for switch in switches:
    # set for output
    GPIO.setup(switch.pin, GPIO.OUT)
    GPIO.output(switch.pin, 1)
    switch.state = "0"

# create flask app to run web server
app = Flask(__name__)

# default handler, if no path is given
@app.route('/')
def index():
    return 'python-dogcollar'

# switch handler
@app.route('/switch/<string:name>/<string:action>')
def action(name, action):
    if action == "on":
        for switch in switches:
            if switch.name == name:
                switch.on()
                return switch.status()
    elif action == "off":
        for switch in switches:
            if switch.name == name:
                switch.off()
                return switch.status()
    elif action == "toggle":
        for switch in switches:
            if switch.name == name:
                switch.toggle()
                return switch.status()
    elif action == "status":
        for switch in switches:
            if switch.name == name:
                return switch.status()
    else:
        return "Valid actions: on/off/toggle/status."

# run the app locally on serverport
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=serverport,)