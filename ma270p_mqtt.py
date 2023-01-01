"""meshArm 270 PI MQTT interface driver
"""
import sys
import paho.mqtt.client as mqtt
import yaml
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle


DEFAULT_CONFIG_FILE = './config.yaml'
MESHARM_DRIVER_PORT = '/dev/ttyAMA0'
# MESHARM_PORT_SPEED = 115200
MESHARM_PORT_SPEED = 1000000


class Config(object):
    """Configuration data
    """

    def __init__(self, conf):
        self._conf = conf

        # broker information
        broker = self._conf.get('broker')
        if broker is None:
            raise ValueError('ERROR: Config: undefined broker')
        self.host = broker.get('host')
        self.port = broker.get('port')

        # topic information
        topic = self._conf.get('topic')
        if topic is None:
            raise ValueError('ERROR: Config: undefined topic')
        self.topic_sub = topic.get('mesharm_sub')
        self.topic_pub = topic.get('mesharm_pub')


class MeshArm270(object):
    """meshArm 270 class
    """

    def __init__(self, pub):
        self._m = MyCobot(MESHARM_DRIVER_PORT, MESHARM_PORT_SPEED)
        self._pub = pub

    def _str_to_id(self, id_str):
        val = None
        if id_str == 'J1':
            val = Angle.J1.value
        elif id_str == 'J2':
            val = Angle.J2.value
        elif id_str == 'J3':
            val = Angle.J3.value
        elif id_str == 'J4':
            val = Angle.J4.value
        elif id_str == 'J5':
            val = Angle.J5.value
        elif id_str == 'J6':
            val = Angle.J6.value

        return val

    def call(self, params):
        cmd = params[0]
        result = ''
        if cmd == 'power_on':
            self._m.power_on()
            result = 'OK'
        elif cmd == 'power_off':
            self._m.power_off()
            result = 'OK'
        elif cmd == 'is_power_on':
            val = self._m.is_power_on()
            if val == 1:
                result = 'true'
            elif val == 0:
                result = 'false'
            else:
                result = 'error'
        elif cmd == 'release_all_servos':
            self._m.release_all_servos()
            result = 'OK'
        elif cmd == 'is_controller_connected':
            val = self._m.is_controller_connected()
            if val == 1:
                result = 'connected'
            elif val == 0:
                result = 'not connected'
            else:
                result = 'error'
        elif cmd == 'pause':
            self._m.pause()
            result = 'OK'
        elif cmd == 'stop':
            self._m.stop()
            result = 'OK'
        elif cmd == 'resume':
            self._m.resume()
            result = 'OK'
        elif cmd == 'is_paused':
            val = self._m.is_paused()
            if val == 1:
                result = 'pause'
            elif val == 0:
                result = 'not pause'
            else:
                result = 'error'
        elif cmd == 'get_speed':
            result = self._m.get_speed()
        elif cmd == 'set_speed':
            self._m.set_speed(int(params[-1]))
        elif cmd == 'get_joint_min_angle':
            jid = self._str_to_id(params[1])
            result = self._m.get_joint_min_angle(jid)
        elif cmd == 'get_joint_max_angle':
            jid = self._str_to_id(params[1])
            result = self._m.get_joint_max_angle(jid)
        elif cmd == 'get_angles':
            angles = self._m.get_angles()
            result = ','.join([str(val) for val in angles])
        elif cmd == 'send_angle':
            jid = self._str_to_id(params[1])
            deg = float(params[2])
            speed = int(params[3])
            self._m.send_angle(jid, deg, speed)
            result = 'OK'
        elif cmd == 'send_angles':
            if len(params) != 8:
                result = 'Bad parameter'
            else:
                angles = [float(str_val) for str_val in params[1:7]]
                speed = int(params[7])
                self._m.send_angles(angles, speed)
                result = 'OK'
        elif cmd == 'get_coords':
            vals = self._m.get_coords()
            result = ','.join([str(val) for val in vals])
        else:
            result = 'Unknown command: ' + cmd

        self._pub.send(result)


class MeshArmMqtt(object):
    """MQTT driver
    """

    def __init__(self, config):
        self._config = config


class MeshArmPublisher(MeshArmMqtt):
    """MQTT Publisher
    """

    def __init__(self, config):
        super().__init__(config)
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_publish  = self._on_publish

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
        self._client.publish(self._config.topic_pub, msg)


class MeshArmSubscriber(MeshArmMqtt):
    """MQTT Subscriber
    """

    def __init__(self, config, mesh_arm):
        super().__init__(config)
        self._mesh_arm = mesh_arm
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    def _on_connect(self, client, userdata, flag, rc):
        print('[sub] Connected with result code ' + str(rc) +
              ' topic: ' + self._config.topic_sub)
        client.subscribe(self._config.topic_sub)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print('[sub] Unexpected disconnection.')

    def _on_message(self, client, userdata, msg):
        msg_str = msg.payload.decode('utf-8')
        print('[sub] Received message: ' + msg_str)
        self._mesh_arm.call(msg_str.split(','))

    def run(self):
        self._client.connect(self._config.host, self._config.port, 60)
        self._client.loop_forever()


if __name__ == '__main__':
    config_file = DEFAULT_CONFIG_FILE
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]

    config = None
    with open(config_file, 'r') as f:
        conf_obj = yaml.safe_load(f)
        config = Config(conf_obj)

    pub = MeshArmPublisher(config)
    mesh_arm = MeshArm270(pub)
    sub = MeshArmSubscriber(config, mesh_arm)

    sub.run()



