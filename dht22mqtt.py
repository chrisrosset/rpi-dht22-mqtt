#!/usr/bin/env python

import logging
import os
import platform
import sys
import time
import traceback

import Adafruit_DHT
import paho.mqtt.client as mqtt

import config

def read(pin):
    h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    return {
        "humidity": h,
        "temperature": t
    }

def timed_read(cfg):
    time.sleep(cfg["interval"])
    return read(cfg["pin"])

def mqtt_topic(key, location):
    return "/{0}/{1}".format(key, location)

def publish_mqtt(client, data, cfg):
    for key in data:
        topic = mqtt_topic(key, cfg["location"])
        client.publish(topic, data[key])

def client_id(cfg):
    return platform.node() + "-" + cfg["location"]

def on_connect(client, userdata, flags, rc):
    logging.info("Connected to the MQTT broker. rc=" + str(rc))

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected from the MQTT broker. rc=" + str(rc))

def mean(l):
    return round(float(sum(l)) / max(len(l), 1), 1)

def setup_logging():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.DEBUG)
    logging.info("Logger set up.")

def main():
    setup_logging()

    try:
        cfg = config.config

        logging.info("Read service configuration cfg = %s", str(cfg))

        client = mqtt.Client(client_id=client_id(cfg))
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.connect(cfg["broker"]["host"])
        client.loop_start()

        i = 0
        samples = cfg["average"]

        running = read(cfg["pin"])
        for key in running:
            running[key] = [running[key]] * samples

        while True:
            data = timed_read(cfg)

            for key in running:
                running[key][i] = data[key]

            i = (i + 1) % samples

            for key in data:
                data[key] = mean(running[key])

            publish_mqtt(client, data, cfg)

    except Exception as e:
        logging.error("Exception thrown.", exc_info=1)
        logging.info("Terminating process.")
        sys.exit(1)

if __name__ == "__main__":
    main()
