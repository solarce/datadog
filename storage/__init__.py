from influxdb import InfluxDBClient
import settings

client = InfluxDBClient(settings.INFLUX_HOST, settings.INFLUX_PORT, settings.INFLUX_USER, settings.INFLUX_PASSWORD, settings.INFLUX_DB, timeout=5)
