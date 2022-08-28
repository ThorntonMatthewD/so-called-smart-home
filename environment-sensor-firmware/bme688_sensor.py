import time
import board
import adafruit_bme680
import busio

SCL_PIN = board.GP1
SDA_PIN = board.GP0
I2C_ADDRESS = 0x77

TEMPERATURE_OFFSET = -2

i2c = busio.I2C(scl=SCL_PIN, sda=SDA_PIN)

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, I2C_ADDRESS)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Set the humidity baseline to 40%, an optimal indoor humidity.
HUMIDITY_BASELINE = 40.0
# This sets the balance between humidity and gas reading in the
# calculation of air_quality_score (25:75, humidity:gas)
HUMIDITY_WEIGHTING = 0.25

burn_in_data = []


def set_gas_burn_in_value():
    """
    Takes samples for 5 minutes and uses last 50 values to calculate gas_baseline
    Mostly taken from the following:
    https://github.com/pimoroni/bme680-python/blob/master/examples/indoor-air-quality.py#L44
    """
    start_time = time.time()
    curr_time = time.time()
    burn_in_time = 300

    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        gas = bme680.gas
        burn_in_data.append(gas)
        time.sleep(1)

    return sum(burn_in_data[-50:]) / 50.0


def calculate_air_quality(gas_baseline, gas, humidity):
    """
    Calculates Air Quality Index (AQI) given current sensor data.
    """
    gas_offset = gas_baseline - gas
    hum_offset = humidity - HUMIDITY_BASELINE

    # Calculate hum_score as the distance from the hum_baseline.
    if hum_offset > 0:
        hum_score = 100 - HUMIDITY_BASELINE - hum_offset
        hum_score /= 100 - HUMIDITY_BASELINE
        hum_score *= HUMIDITY_WEIGHTING * 100

    else:
        hum_score = HUMIDITY_BASELINE + hum_offset
        hum_score /= HUMIDITY_BASELINE
        hum_score *= HUMIDITY_WEIGHTING * 100

    # Calculate gas_score as the distance from the gas_baseline.
    if gas_offset > 0:
        gas_score = gas / gas_baseline
        gas_score *= 100 - (HUMIDITY_WEIGHTING * 100)

    else:
        gas_score = 100 - (HUMIDITY_WEIGHTING * 100)

    # Calculate air_quality_score.
    return hum_score + gas_score


def gather_samples(gas_baseline):
    """Places readings from sensor into dict"""
    gas = bme680.gas
    humidity = bme680.relative_humidity

    samples = {
        "temp": bme680.temperature + TEMPERATURE_OFFSET,
        "gas": gas,
        "rel_humidity": humidity,
        "altitude": bme680.altitude,
        "pressure": bme680.pressure,
    }

    samples.update(air_quality=calculate_air_quality(gas_baseline, gas, humidity))

    return samples


def application_loop():
    """This is the main application loop."""
    try:
        gas_baseline = set_gas_burn_in_value()

        while True:
            print(gather_samples(gas_baseline))
            time.sleep(5)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    application_loop()
