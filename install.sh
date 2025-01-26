#!/bin/bash

set -e  # Exit on errors

echo "Running Docker installation..."
./scripts/install_docker.sh

echo "Running application setup..."
./scripts/setup.sh

echo "Installation complete! Please log out and back in to apply changes."
