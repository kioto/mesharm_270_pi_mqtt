"""meshArm 270 PI MQTT Publisher
"""
import paho.mqtt.client as mqtt


class MeshArmPublisher(object):
    """MQTT Publisher
    """

    def __init__(self, config, queue, attr):
        self._config = config
        self._queue = queue
        if attr == 'server':
            self._topic = self._config.topic_response
        elif attr == 'client':
            self._topic = self._config.topic_command
        else:
            raise ValueError('Bad attr: ' + attr)

        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish = self._on_publish

        self._client.connect(self._config.host, self._config.port, 60)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flag, rc):
        print('[pub] Connected with result code ' + str(rc))

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print('[pub] Unexpected disconnection.')

    def _on_publish(self, client, userdata, mid):
        print('[pub] publish: ' + str(mid))

    def send(self, msg):
        print('send', msg)
        self._client.publish(self._topic, msg)


class ServerPublisher(MeshArmPublisher):
    """Server Publisher
    """

    def __init__(self, config, queue):
        super().__init__(config, queue, 'server')


class ClientPublisher(MeshArmPublisher):
    """Client Publisher
    """

    def __init__(self, config, queue):
        super().__init__(config, queue, 'client')
