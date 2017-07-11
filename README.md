# rpi-dht22-mqtt

Read DHT22 data on a Raspberry Pi and publish over MQTT.

## Usage

Settings are specified in `config.py` which needs to be mounted into the docker
container that the application will run.

```bash
mkdir cfg
cp config.example.py cfg/config.py

vi cfg/config.py # set up your config

docker build -t dht22mqtt .
docker run \
    -d \
    -v $(pwd)/cfg/config.py:/app/config.py \
    --restart always \
    --net=host \
    --privileged \
    --cap-add SYS_RAWIO \
    --device=/dev/mem dht22mqtt
```
