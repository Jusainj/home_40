#!/bin/bash

# Function to create .env file
create_env_file() {
  env_file=".env"

  if [ -f "$env_file" ]; then
    echo "$env_file already exists. Skipping creation."
    return
  fi

  echo "Creating .env file..."

  # Define default values for other variables
  mqtt_host="mqtt-broker"
  influxdb_db="sensor_data"
  influxdb_user="admin"
  influxdb_password=""

  # Get user input for environment variables
  read -p "Enter MQTT Broker Host (default: $mqtt_host): " mqtt_broker
  mqtt_broker=${mqtt_broker:-$mqtt_host}

  read -p "Enter MQTT Port (default: 1883): " mqtt_port
  mqtt_port=${mqtt_port:-1883}

  read -p "Enter InfluxDB database name (default: $influxdb_db): " influxdb_db_input
  influxdb_db=${influxdb_db_input:-$influxdb_db}

  read -p "Enter InfluxDB admin username (default: $influxdb_user): " influxdb_user_input
  influxdb_user=${influxdb_user_input:-$influxdb_user}

  # InfluxDB password will be left empty for manual setup
  echo "Leave the password fields empty and manually configure them later."

  # Write to .env file with empty password fields
  cat <<EOF >"$env_file"
MQTT_BROKER=$mqtt_broker
MQTT_PORT=$mqtt_port
INFLUXDB_DB=$influxdb_db
INFLUXDB_ADMIN_USER=$influxdb_user
INFLUXDB_ADMIN_PASSWORD=$influxdb_password
EOF

  echo "$env_file created successfully."
}

# Function to ensure required directories exist
ensure_directories() {
  directories=("grafana_data" "influxdb")

  for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
      echo "Creating directory: $dir"
      mkdir -p "$dir"
    else
      echo "Directory already exists: $dir"
    fi
  done

  # Set correct permissions for grafana directory
  echo "Setting correct permissions for grafana/data..."
  sudo chmod -v a+rwx grafana/data
}

# Main setup function
main() {
  echo "Starting setup..."
  create_env_file
  ensure_directories
  echo "Setup complete!"
}

# Run the main function
main
