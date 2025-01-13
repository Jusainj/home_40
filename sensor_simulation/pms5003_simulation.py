import os
import time
import random
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

load_dotenv(os.path.abspath('../.env'))

# MySQL Database configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}

# Simulation parameters
SIMULATION_DURATION = 60  # in seconds
DATA_FREQUENCY = 1.5  # records per second (approximately)

# Connect to MySQL
def connect_to_mysql():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**MYSQL_CONFIG)


# Initialize MySQL storage
def initialize_mysql_storage():
    """Creates the necessary MySQL table if it doesn't exist."""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pm_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp INT NOT NULL,
            pm2_5 INT NOT NULL,
            pm10 INT NOT NULL
        )
        """
    )
    connection.commit()
    cursor.close()
    connection.close()


# Save data to MySQL
def save_to_mysql(record):
    """Inserts a record into the MySQL database."""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO pm_data (timestamp, pm2_5, pm10) VALUES (%s, %s, %s)",
        (record["timestamp"], record["pm2_5"], record["pm10"])
    )
    connection.commit()
    cursor.close()
    connection.close()


# Fetch data from MySQL for visualization
def fetch_from_mysql():
    """Fetches all data from MySQL."""
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT timestamp, pm2_5, pm10 FROM pm_data ORDER BY id")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Generate simulated data
def simulate_data():
    """Simulates PM2.5 and PM10 data."""
    pm2_5 = random.randint(5, 150)  # Simulate PM2.5 values (5-150 µg/m³)
    pm10 = random.randint(10, 200)  # Simulate PM10 values (10-200 µg/m³)
    timestamp = int(time.mktime(datetime.utcnow().timetuple()))
    return {"timestamp": timestamp, "pm2_5": pm2_5, "pm10": pm10}


# Visualization setup
def update_plot(frame, mysql_data, ax1, ax2):
    """Updates the real-time plot."""
    mysql_timestamps, mysql_pm2_5, mysql_pm10 = zip(*mysql_data) if mysql_data else ([], [], [])

    mysql_timestamps = [datetime.fromtimestamp(ts) for ts in mysql_timestamps]

    ax1.clear()
    ax2.clear()

    ax1.plot(mysql_timestamps, mysql_pm2_5, label="MySQL PM2.5 (µg/m³)", color="blue")

    ax2.plot(mysql_timestamps, mysql_pm10, label="MySQL PM10 (µg/m³)", color="green")

    ax1.legend(loc="upper right")
    ax2.legend(loc="upper right")
    ax1.set_title("Real-time PM2.5 and PM10 Levels")
    ax1.set_ylabel("PM2.5 (µg/m³)")
    ax2.set_ylabel("PM10 (µg/m³)")
    ax2.set_xlabel("Time")
    plt.tight_layout()

# Main simulation loop
def run_simulation():
    """Runs the simulation for the specified duration."""
    initialize_mysql_storage()
    # influx_client = connect_to_influxdb()
    start_time = time.time()
    print("Starting simulation...")
    while time.time() - start_time < SIMULATION_DURATION:
        record = simulate_data()
        save_to_mysql(record)
        print(f"Recorded data: PM2.5={record['pm2_5']} µg/m³, PM10={record['pm10']} µg/m³")
        time.sleep(1 / DATA_FREQUENCY)

# Real-time visualization
def visualize_data():
    """Visualizes the data in real time."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    # influx_client = connect_to_influxdb()

    def update(frame):
        mysql_data = fetch_from_mysql()
        # influxdb_data = fetch_from_influxdb(influx_client)
        update_plot(frame, mysql_data, ax1, ax2)

    animation = FuncAnimation(fig, update, interval=1000)
    plt.show()

if __name__ == "__main__":
    run_simulation()
    visualize_data()
