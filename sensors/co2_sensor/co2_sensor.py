#!/usr/bin/python

import datetime
import serial
import paho.mqtt.client as mqtt
from binascii import hexlify
import json
import os
import time

# MQTT Settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = "sensor/co2"

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Open Serial Port
with serial.Serial("/dev/ttyUSB0", 9600, timeout=5) as ser:
    while True:
        ser.reset_input_buffer()  # Flush old data
        time.sleep(0.1)  # Small delay to ensure fresh read

        # Read CO2 Sensor Data
        b = ser.read(16)
        timestamp = int(time.time())

        if len(b) == 16:
            ppm = b[6:8]
            ppm_value = int(ppm[0]) * 256 + int(ppm[1])

            # Create JSON payload
            payload = {
                "timestamp": timestamp,
                "sensor_id": "co2_sensor",
                "co2_ppm": ppm_value
            }
            payload_json = json.dumps(payload)

            # Publish fresh data
            mqtt_client.publish(MQTT_TOPIC, payload_json, retain=False)
            print(f"Published: {payload_json}")

        else:
            print(f"{timestamp} - Invalid packet received: {hexlify(b)}")

        time.sleep(2)  # Read every 2 seconds

