import paho.mqtt.client as mqtt
 
def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("drone/001")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_message(client, userdata, msg):
    print("Received message '"
          + str(msg.payload)
          + "' on topic '" + msg.topic
          + "' with QoS " + str(msg.qos))


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
 
client.connect('192.168.1.7', 1883, 60)
 
client.loop_forever()
