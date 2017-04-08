#!/usr/bin/env python

import platform
import time

import Adafruit_DHT
import paho.mqtt.client as mqtt

import config

def read():
    h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "4")
    return {
        "humidity": round(h, 1),
        "temperature": round(t, 1)
    }

def timed_read(cfg):
    time.sleep(cfg["interval"])
    return read()

def mqtt_topic(key, location):
    return "/{0}/{1}".format(key, location)

def publish_mqtt(client, data, cfg):
    for key in data:
        topic = mqtt_topic(key, cfg["location"])
        client.publish(topic, data[key])

def client_id(cfg):
    return platform.node() + "-" + cfg["location"]

def on_connect():
    print("Connected with rc=" + str(rc))

def mean(l):
    return float(sum(l)) / max(len(l), 1)

def main():

    cfg = config.config

    client = mqtt.Client(client_id=client_id(cfg))
    client.on_connect = on_connect
    client.connect(cfg["broker"]["host"])

    i = 0
    samples = cfg["average"]

    running = read()
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

if __name__ == "__main__":
    main()
