# python-dogcollar

A Python app used to control a remote dog training collar (beep, vibrate, and static). The app creates a simple REST API with Flask that is compatible with [HomeBridge](https://github.com/nfarina/homebridge) via the [homebridge-http-switch](https://github.com/Supereg/homebridge-http-switch) plugin.

I created this because I catch my nearly always well-behaved dog doing things that she shouldn't on occasion. I find that I only need to use the beep and vibrate modes with her to keep her in check when I'm not at home and checking up on her with cameras.

**NOTE: My Raspberry Pi is connect to a relay HAT. Relays typically require LOW power to be *ON* so the GPIO ON/OFF is reversed in the Python script. You would want to change it if you'd like to use the script for other purposes.**

## Setup

This is running on a Raspberry Pi 3b+ using a fresh install of Raspian Buster 4.19 and Python 3.7.3.

#### Python 3 Virtual Environment

Set up a Python 3 virtual environment.

````sh
python3 -m venv ~/venv/python-dogcollar
````

and activate it...

````sh
. ~/venv/python-dogcollar/bin/activate
````

#### Clone the Git Repository

````sh
git clone git@github.com:dionmunk/python-dogcollar.git
````

#### Install the Requirements

Navigate to the directory where you cloned the Git repository so that you can see the `requirements.txt` file.

````sh
pip3 install -r requirements.txt
````

#### Run the App

The shell script automatically activates the virtual environment if you created it in the default location.

````sh
./dogcollar.sh
````

## Usage

You will want to modify the `config.json` file to fit your preferences. Each pin must have a name and pin associated with it to perform operations. The config file in this repository is set up to work with a [3 Relay Expansion Module](https://amzn.to/38wlagr) for the Raspberry Pi.

#### URLs

The switches/relays can be controlled using the following URL scheme, where name is the name you put into the config file, and action is the action you would like to perform (on/off/toggle/status).

```
GET /switch/<name>/<action>
```

## HomeBridge Configuration

Because the app has a duration where it will turn the switch on and then off after a few seconds, these are considered *stateless* switches. They can be set up in your HomeBridge config file as accessories with the following bit of code.

```json
"accessories": [
    {
        "accessory": "HTTP-SWITCH",
        "name": "Dog Collar Beep",
        "switchType": "stateless",
        "timeout": 3000,
        "onUrl": "http://192.168.0.5:8080/switch/beep/on"
    }
]
```