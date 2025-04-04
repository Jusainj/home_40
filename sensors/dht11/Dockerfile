FROM python:3.9-slim

WORKDIR /app

COPY co2_sensor.py /app/co2_sensor.py

RUN pip install adafruit-circuitpython-dht paho-mqtt

CMD ["python", "/app/publish_dht11.py"]

