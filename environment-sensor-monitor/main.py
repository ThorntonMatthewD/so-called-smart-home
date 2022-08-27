import io
import os
import json

import util
import logger
import client


TTY_PORT = os.environ.get("ENVIRO_SENSOR_PORT") or "/dev/ttyACM0"

tty = io.TextIOWrapper(io.FileIO(os.open(TTY_PORT, os.O_NOCTTY | os.O_RDWR), "r"))
prom_client = client.Client()

for line in iter(tty.readline, None):
    if len(line) > 1:
        try:
            data = json.loads(util.clean_tty_line(line))
            prom_client.update_gauges(data)
        except json.decoder.JSONDecodeError as e:
            logger.log_error(e, f"Could not read: {line}")
