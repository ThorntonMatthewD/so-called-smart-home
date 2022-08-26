import time
import board
import adafruit_bme680
import busio

SCL_PIN = board.GP1
SDA_PIN = board.GP0
I2C_ADDRESS = 0x77

i2c = busio.I2C(scl=SCL_PIN, sda=SDA_PIN)

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, I2C_ADDRESS)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

TEMPERATURE_OFFSET = -2


def gather_samples():
    """Places readings from sensor into dict"""
    return {
        "temp": bme680.temperature + TEMPERATURE_OFFSET,
        "gas": bme680.gas,
        "rel_humidity": bme680.relative_humidity,
        "altitude": bme680.altitude,
        "pressure": bme680.pressure,
    }


while True:
    print(gather_samples())
    time.sleep(5)
