# server.py
from flask import Flask
from gevent.pywsgi import WSGIServer
import subprocess
import copy

app = Flask(__name__)

GPIO_PIN = "23"

commands = {
    "get_hdmi_state": ["vcgencmd", "display_power"],
    "set_hdmi_state": ["vcgencmd", "display_power"], # either 1 (on) or 0 (off)
    "get_backlight_state": ["raspi-gpio", "get", GPIO_PIN],
    "set_backlight_state": ["raspi-gpio", "set", GPIO_PIN, "op"], #either dh (high, on) or dl (low, off)
}

@app.get("/state/backlight")
def get_backlight_state():
    command = commands.get("get_backlight_state")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

@app.get("/state/hdmi")
def get_hdmi_state():
    command = commands.get("get_hdmi_state")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

@app.post("/state/backlight/off")
def turn_off_backlight():
    command = copy.deepcopy(commands.get("set_backlight_state"))
    command.append("dl")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

@app.post("/state/backlight/on")
def turn_on_backlight():
    command = copy.deepcopy(commands.get("set_backlight_state"))
    command.append("dh")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

@app.post("/state/hdmi/off")
def turn_off_hdmi():
    command = copy.deepcopy(commands.get("set_hdmi_state"))
    command.append("0")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

@app.post("/state/hdmi/on")
def turn_on_hdmi():
    command = copy.deepcopy(commands.get("set_hdmi_state"))
    command.append("1")
    print ("Executing command: ", command)
    return subprocess.check_output(command)

if __name__ == "__main__":
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
