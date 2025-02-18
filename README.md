# home_40
![pms5003_architecture drawio](https://github.com/user-attachments/assets/8c3f5529-514a-43fd-93db-3e867709ef37)

## Overview
This setup enables the following functionalities:

* CO₂ Sensor: Collects CO₂ data and sends it to an MQTT broker.
* PMS5003 Sensor: Collects particulate matter (PM) data and sends it to the MQTT broker.
* MQTT Broker: Manages communication between devices and other services using the MQTT protocol.
* InfluxDB: Stores sensor data in a time-series database.
* Telegraf: Collects data from the MQTT broker and stores it in InfluxDB.
* Grafana: Visualizes the data stored in InfluxDB with customizable dashboards.

## Introduction
1. Run setup script to install required software, files and directories
```
chmod +x install.sh
chmod +x scripts/*.sh

./install.sh
```

2. To check: Does `./grafana/data` folder exist in local project directory? If not, please create it.

3. Add your custom password to `.env` to secure your influxdb database.

4. Start docker compose in detached mode
```
docker-compose build
docker-compose up -d

```
5. Stop docker compose
```
docker-compose down
```

## Please note
- serial ports on the raspi might differ from type to type. In case port cannot be found, please change it in the sensor scripts like: `pms5003/read_pms5003.py`.
- If your port is not 'dev/ttyS0' then change your port in the sensor script as well as this configuration: `docker-compose.yaml`.


## Setup Sensor
In case this is the first time using the sensor on a raspberryPi, the Serial Interface must be enabled first.
1. open raspi config
```
$ sudo raspi-config
```
2. Navigate to `Interfacing Options` > `Serial` and enable the serial interface.
3. Disable shell acess over serial when prompted.
4. Restart by: `$ sudo reboot`.

## Test sensor
- to dryrun the sensor using only a python script, please refer to `test/*` and:
* install dependecies `pip install -r requirements.txt`
* run the sensor script `python read_pms5003_test.py`
