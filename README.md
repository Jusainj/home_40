# home_40

## Introduction
1. Run setup script to install required software, files and directories
```
chmod +x install.sh
chmod +x scripts/*.sh

./install.sh
```

2. To check: Does ./mysql_data, ./grafana_data folder exist in local project directory?

3. Start docker compose is deteched mode
```
docker-compose build

docker-compose up -d

```
4. Stop docker compose
```
docker-compose down
```

## Please note
- serial ports on the raspi might differ from type to type. In case port cannot be found, please change it in `pms5003/read_pms5003.py`.
- If your port is not 'dev/ttyS0' then also change your port with this configuration in `docker-compose.yaml`  

## Test sensor
- to dryrun the sensor using only a python script, please refer to `test/*` and:
* install dependecies `pip install -r requirements.txt`
* run the sensor script `python read_pms5003_test.py`
