import os
from prometheus_client import CollectorRegistry, Gauge, start_http_server

# Something ludicrous that can be filtered out if any of the sensors fail
FALLBACK_VALUE = -1000000
CLIENT_PORT = int(os.environ.get("ENVIRO_PROMETHEUS_METRICS_PORT") or 8090)


class Client:
    """Client to expose metrics to Prometheus"""

    def __init__(self):
        self.registry = CollectorRegistry()
        start_http_server(CLIENT_PORT)

        self.temp_gauge = Gauge(
            "current_temperature", "Current temperature (degrees celsius)"
        )
        self.gas_gauge = Gauge(
            "current_gas_resistance", "Current gas resistance (ohms)"
        )
        self.humidity_gauge = Gauge(
            "current_relative_humidity", "Current relative humidity (%)"
        )
        self.altitude_gauge = Gauge("current_altitude", "Current altitude (meters)")
        self.pressure_gauge = Gauge(
            "current_pressure", "Current barometric pressure (hPa)"
        )

    def update_gauges(self, sensor_data: dict) -> None:
        """Updates values of the gauges from sensor reading data"""
        self.temp_gauge.set(sensor_data.get("temp", FALLBACK_VALUE))
        self.gas_gauge.set(sensor_data.get("gas", FALLBACK_VALUE))
        self.humidity_gauge.set(sensor_data.get("rel_humidity", FALLBACK_VALUE))
        self.altitude_gauge.set(sensor_data.get("altitude", FALLBACK_VALUE))
        self.pressure_gauge.set(sensor_data.get("pressure", FALLBACK_VALUE))
