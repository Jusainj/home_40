import os
import serial
import struct
import time
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENSOR_READ_FREQUENCY = 1  # request records per second
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}
serial_port = '/dev/ttyAMA0'

# Connect to MySQL
def connect_to_mysql():
    return mysql.connector.connect(**MYSQL_CONFIG)


# Initialize MySQL storage
def initialize_mysql_storage():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pm_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp INT NOT NULL,
            pm1_0 INT NOT NULL,
            pm2_5 INT NOT NULL,
            pm10 INT NOT NULL,
            particle_0_3 INT NOT NULL,
            particle_0_5 INT NOT NULL,
            particle_1_0 INT NOT NULL,
            particle_2_5 INT NOT NULL
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()


# Save data to MySQL
def save_to_mysql(record):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO pm_data (timestamp, pm1_0, pm2_5, pm10, particle_0_3, particle_0_5, particle_1_0, particle_2_5)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record["timestamp"], record["pm1_0"], record["pm2_5"], record["pm10"],
        record["particle_0_3"], record["particle_0_5"], record["particle_1_0"], record["particle_2_5"]
    ))
    connection.commit()
    cursor.close()
    connection.close()


# Function to validate the checksum (a simple sum of bytes)
def validate_checksum(data):
    checksum_calculated = sum(data[:-2]) & 0xFFFF
    checksum_received = struct.unpack('>H', data[30:32])[0]
    return checksum_calculated == checksum_received


# Read data from PMS5003
def read_pms5003():
    try:
        with serial.Serial(serial_port, baudrate=9600, timeout=2) as ser:
            while True:
                data = ser.read(32)
                if not validate_checksum(data):
                    print("Error: Invalid checksum!")
                    continue

                if data[0:2] == b'\x42\x4d':
                    pm2_5 = struct.unpack('>H', data[6:8])[0]  # PM2.5 value
                    pm10 = struct.unpack('>H', data[8:10])[0]  # PM10 value
                    pm1_0 = struct.unpack('>H', data[10:12])[0]  # PM1.0 value
                    particle_counts = struct.unpack('>HHHH', data[12:20])

                    timestamp = timestamp = int(time.time())
                    record = {
                        "timestamp": timestamp,
                        "pm1_0": pm1_0,
                        "pm2_5": pm2_5,
                        "pm10": pm10,
                        "particle_0_3": particle_counts[0],
                        "particle_0_5": particle_counts[1],
                        "particle_1_0": particle_counts[2],
                        "particle_2_5": particle_counts[3],
                    }

                    save_to_mysql(record)
                    print(f"Saved data: {record}")
                time.sleep(SENSOR_READ_FREQUENCY)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    initialize_mysql_storage()
    read_pms5003()
