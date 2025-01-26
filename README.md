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