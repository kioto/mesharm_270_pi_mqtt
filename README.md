# mesharm_270_pi_mqtt
meshArm 270 PI MQTT interface

## Usage

Start server.

```
sudo /home/ubuntu/py37env/bin/python ma270p_mqtt.py
```

Monitoring MQTT broker.

```
mosquitto_sub -h 192.168.1.7 -t meshArm270PI/command

or

mosquitto_sub -h 192.168.1.7 -t meshArm270PI/response
```

Send command.

```
mosquitto_pub -h 192.168.1.7 -t meshArm270PI/command -m get_angles
```
