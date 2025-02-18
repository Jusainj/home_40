FROM python:3.9-slim

WORKDIR /app

COPY co2_sensor.py /app/co2_sensor.py

RUN pip install paho-mqtt pyserial

CMD ["python", "/app/co2_sensor.py"]

