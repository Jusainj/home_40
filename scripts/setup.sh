#!/bin/bash

# Function to create .env file
create_env_file() {
  env_file=".env"

  if [ -f "$env_file" ]; then
    echo "$env_file already exists. Skipping creation."
    return
  fi

  echo "Creating .env file..."
  mysql_host="mysql"

  read -p "Enter MySQL username (default: root): " mysql_user
  mysql_user=${mysql_user:-root}

  read -sp "Enter MySQL password: " mysql_password
  echo
  read -p "Enter MySQL database name: " mysql_database

  cat <<EOF >"$env_file"
MYSQL_HOST=$mysql_host
MYSQL_USER=$mysql_user
MYSQL_PASSWORD=$mysql_password
MYSQL_DATABASE=$mysql_database
EOF

  echo "$env_file created successfully."
}

# Function to ensure required directories exist
ensure_directories() {
  directories=("mysql_data" "grafana_data")

  for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
      echo "Creating directory: $dir"
      mkdir -p "$dir"
    else
      echo "Directory already exists: $dir"
    fi
  done

  # Set correct permissions
  echo "Setting correct permissions..."
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
