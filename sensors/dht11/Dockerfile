FROM python:3.9

# Install system dependencies, including libgpiod2 for GPIO access
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libgpiod2 \
    && pip install --upgrade pip \
    && pip install RPi.GPIO board adafruit-circuitpython-dht paho-mqtt

WORKDIR /app

COPY publish_dht11.py /app/publish_dht11.py

CMD ["python", "/app/publish_dht11.py"]

