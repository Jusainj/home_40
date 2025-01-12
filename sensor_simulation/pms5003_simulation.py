import os
import time
import random
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# File to store the simulated data
current_path = os.getcwd()
DATA_FILE = f"{current_path}/../shared_data/sensor_data.csv"

# Simulation parameters
SIMULATION_DURATION = 60  # in seconds
DATA_FREQUENCY = 1.5  # records per second (approximately)

# Generate simulated data
def simulate_data():
    """Simulates PM2.5 and PM10 data."""
    pm2_5 = random.randint(5, 150)  # Simulate PM2.5 values (5-150 µg/m³)
    pm10 = random.randint(10, 200)  # Simulate PM10 values (10-200 µg/m³)
    timestamp = int(time.mktime(datetime.utcnow().timetuple()))
    return {"timestamp": timestamp, "pm2_5": pm2_5, "pm10": pm10}

# Initialize CSV storage
def initialize_storage():
    """Creates an empty CSV file with appropriate headers if it doesn't exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Create the file if it doesn't exist
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        pd.DataFrame(columns=["timestamp", "pm2_5", "pm10"]).to_csv(DATA_FILE, index=False)

    try:
        pd.read_csv(DATA_FILE)  # Try to read the file to ensure it exists

    except FileNotFoundError:
        pd.DataFrame(columns=["timestamp", "pm2_5", "pm10"]).to_csv(DATA_FILE, index=False)

# Save data to CSV
def save_data(record):
    """Appends a record to the CSV file."""
    df = pd.DataFrame([record])
    df.to_csv(DATA_FILE, mode="a", header=False, index=False)

# Visualization setup
def update_plot(frame, data, ax1, ax2):
    """Updates the real-time plot."""
    df = pd.read_csv(DATA_FILE)
    if len(df) > 0:
        # Extract latest data for plotting
        timestamps = pd.to_datetime(df["timestamp"], unit="s")
        ax1.clear()
        ax2.clear()
        ax1.plot(timestamps, df["pm2_5"], label="PM2.5 (µg/m³)", color="blue")
        ax2.plot(timestamps, df["pm10"], label="PM10 (µg/m³)", color="green")
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
    initialize_storage()
    start_time = time.time()
    
    print("Starting simulation...")
    while True: # time.time() - start_time < SIMULATION_DURATION:
        record = simulate_data()
        save_data(record)
        print(f"Recorded data: PM2.5={record['pm2_5']} µg/m³, PM10={record['pm10']} µg/m³")
        time.sleep(1 / DATA_FREQUENCY)

# Real-time visualization
def visualize_data():
    """Visualizes the data in real time."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    animation = FuncAnimation(fig, update_plot, fargs=(DATA_FILE, ax1, ax2), interval=1000)
    plt.show()

if __name__ == "__main__":
    run_simulation()
    visualize_data()
