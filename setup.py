#!/usr/bin/env python3

import os

def create_env_file():
    """Create a .env file with MySQL configuration."""
    env_file = ".env"

    if os.path.exists(env_file):
        print(f"{env_file} already exists. Skipping creation.")
        return

    print("Creating .env file...")
    mysql_host = input("Enter MySQL host (default: localhost): ") or "localhost"
    mysql_user = input("Enter MySQL username (default: root): ") or "root"
    mysql_password = input("Enter MySQL password: ")
    mysql_database = input("Enter MySQL database name: ")

    with open(env_file, "w") as f:
        f.write(f"MYSQL_HOST={mysql_host}\n")
        f.write(f"MYSQL_USER={mysql_user}\n")
        f.write(f"MYSQL_PASSWORD={mysql_password}\n")
        f.write(f"MYSQL_DATABASE={mysql_database}\n")

    print(f"{env_file} created successfully.")


def ensure_directories():
    """Ensure required directories exist."""
    directories = ["mysql_data", "grafana_data"]

    for directory in directories:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)
        else:
            print(f"Directory already exists: {directory}")


def main():
    """Main setup script."""
    print("Starting setup...")
    create_env_file()
    ensure_directories()
    print("Setup complete!")

if __name__ == "__main__":
    main()
