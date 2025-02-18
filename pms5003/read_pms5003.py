import os
import serial
import struct
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENSOR_READ_FREQUENCY = 1  # In Sekunden
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "sensor/pm"

serial_port = '/dev/ttyS0'

# Setup MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Funktion zur Validierung der Checksumme
def validate_checksum(data):
    checksum_calculated = sum(data[:-2]) & 0xFFFF
    checksum_received = struct.unpack('>H', data[30:32])[0]
    return checksum_calculated == checksum_received

# Funktion zum Einlesen der PMS5003-Daten
def read_pms5003():
    try:
        with serial.Serial(serial_port, baudrate=9600, timeout=2) as ser:
            while True:
                data = ser.read(32)

                if not validate_checksum(data):
                    print("⚠️ Fehler: Ungültige Checksumme!")
                    continue

                if data[0:2] == b'\x42\x4d':
                    pm2_5 = struct.unpack('>H', data[6:8])[0]
                    pm10 = struct.unpack('>H', data[8:10])[0]
                    pm1_0 = struct.unpack('>H', data[10:12])[0]
                    particle_counts = struct.unpack('>HHHH', data[12:20])

                    timestamp = int(time.time())

                    record = {
                        "timestamp": timestamp,
                        "sensor_id": "pms5003",
                        "pm1_0": pm1_0,
                        "pm2_5": pm2_5,
                        "pm10": pm10,
                        "particle_0_3": particle_counts[0],
                        "particle_0_5": particle_counts[1],
                        "particle_1_0": particle_counts[2],
                        "particle_2_5": particle_counts[3],
                    }

                    # MQTT senden
                    mqtt_client.publish(MQTT_TOPIC, json.dumps(record))
                    print(f"📡 Gesendet: {record}")

                time.sleep(SENSOR_READ_FREQUENCY)

    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    read_pms5003()
