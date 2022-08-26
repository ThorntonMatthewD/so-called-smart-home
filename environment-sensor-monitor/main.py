import io
import os
import json

import util

TTY_PORT = os.environ.get("ENVIRO_SENSOR_PORT") or "/dev/ttyACM0"

tty = io.TextIOWrapper(io.FileIO(os.open(TTY_PORT, os.O_NOCTTY | os.O_RDWR), "r"))


for line in iter(tty.readline, None):
    if len(line) > 1:
        try:
            data = json.loads(util.clean_tty_line(line))
            print(data)
        except json.decoder.JSONDecodeError as e:
            print(f"{line} could not be parsed into JSON")
