FROM resin/rpi-raspbian:latest
ENTRYPOINT []

RUN apt-get update && \
    apt-get -qy install \
        build-essential \
        python-dev \
        python-pip \
        virtualenv

RUN yes | pip install \
        Adafruit_Python_DHT \
        paho-mqtt

RUN mkdir /app
COPY . /app
WORKDIR "/app"

CMD ["python", "dht22mqtt.py"]
