#!/usr/bin/python

import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json
import os

# MQTT Settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = "sensor/dht11"

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Initialize DHT11 sensor (connected to GPIO4)
dht_device = adafruit_dht.DHT11(board.D4)

while True:
    try:
        # Read temperature and humidity from DHT11 sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            timestamp = int(time.time())

            # Create JSON payload
            payload = {
                "timestamp": timestamp,
                "sensor_id": "dht11_sensor",
                "temperature": temperature,
                "humidity": humidity
            }
            payload_json = json.dumps(payload)

            # Publish fresh data to MQTT
            mqtt_client.publish(MQTT_TOPIC, payload_json, retain=False)
            print(f"Published: {payload_json}")

        else:
            print("Failed to retrieve data from DHT11 sensor")

    except RuntimeError as error:
        print(f"Reading error: {error.args[0]}")

    time.sleep(5)
