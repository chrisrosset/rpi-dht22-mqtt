# rpi-dht22-mqtt

Read DHT22 data on a Raspberry Pi and publish over MQTT.

## Usage

Settings are specified in `config.py`. You can either bundle this file into your image or mount one into docker.

```
docker build -t dht22mqtt .
docker run -d --restart always --net=host --cap-add SYS_RAWIO --device=/dev/mem dht22mqtt
```
