"""meshArm 270 PI MQTT Subscriber
"""
import threading
import paho.mqtt.client as mqtt


class MeshArmSubscriber(object):
    """MQTT Subscriber
    """

    def __init__(self, config, queue, attr):
        self._config = config
        self._queue = queue
        if attr == 'server':
            self._topic = self._config.topic_command
        elif attr == 'client':
            self._topic = self._config.topic_response
        else:
            raise ValueError('Bad attr: ' + attr)

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    def _on_connect(self, client, userdata, flag, rc):
        print('[sub] Connected with result code ' + str(rc) +
              ' topic: ' + self._topic)
        client.subscribe(self._topic)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print('[sub] Unexpected disconnection.')

    def _on_message(self, client, userdata, msg):
        msg_str = msg.payload.decode('utf-8')
        print('[sub] Received message: ' + msg_str)
        self._queue.put(msg_str.split(','))

    def _worker(self):
        self._client.connect(self._config.host, self._config.port, 60)
        self._client.loop_forever()

    def run(self):
        threading.Thread(target=self._worker, daemon=True).start()


class ServerSubscriber(MeshArmSubscriber):
    """Server Subscriber
    """

    def __init__(self, config, queue):
        super().__init__(config, queue, 'server')


class ClientSubscriber(MeshArmSubscriber):
    """Client Subscriber
    """

    def __init__(self, config, queue):
        super().__init__(config, queue, 'client')
