#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to install Docker
install_docker() {
  echo "Checking if Docker is installed..."
  if command_exists docker; then
    echo "Docker is already installed. Skipping installation."
  else
    echo "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    echo "Docker installed successfully."
    rm -f get-docker.sh
  fi
}

# Function to install Docker Compose
install_docker_compose() {
  echo "Checking if Docker Compose is installed..."
  if command_exists docker-compose; then
    echo "Docker Compose is already installed. Skipping installation."
  else
    echo "Docker Compose is not installed. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully."
  fi
}

# Function to add the current user to the Docker group
configure_docker_user() {
  echo "Configuring Docker permissions for the current user..."
  if groups | grep -q "\bdocker\b"; then
    echo "User is already in the Docker group. No changes needed."
  else
    echo "Adding user to the Docker group..."
    sudo usermod -aG docker "$USER"
    echo "Please log out and back in to apply the group changes."
  fi
}

# Main script execution
main() {
  echo "Starting installation of Docker and Docker Compose..."
  install_docker
  install_docker_compose
  configure_docker_user
  echo "Installation complete. Docker and Docker Compose are ready to use."
}

main
