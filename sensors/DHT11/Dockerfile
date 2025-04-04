FROM python:3.9-slim

WORKDIR /app

COPY publish_dht11.py /app/publish_dht11.py


RUN pip install adafruit-circuitpython-dht paho-mqtt

CMD ["python", "/app/publish_dht11.py"]

