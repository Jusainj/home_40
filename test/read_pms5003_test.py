import serial
import struct
import time

SENSOR_READ_FREQUENCY = 1  # request records per second
serial_port = '/dev/ttyAMA0'

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
                    print(f"Recorded data: {record}")
                time.sleep(SENSOR_READ_FREQUENCY)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    read_pms5003()
