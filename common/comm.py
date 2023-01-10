"""通信モジュール
"""
import time
import queue
from subscriber import ClientSubscriber
from publisher import ClientPublisher


JOINTS = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6']


class ClientComm(object):

    def __init__(self, config):
        self._config = config
        self._queue = queue.Queue()
        self._sub = ClientSubscriber(self._config, self._queue)
        self._sub.run()
        self._pub = ClientPublisher(self._config, self._queue)

        # reset queue
        while self._queue.empty() is False:
            self._queue.get()
            self._queue.task_done()

    def _send(self, msg):
        self._pub.send(msg)
        while self._queue.empty():
            pass
        ret = self._queue.get()
        print('Received', ret)
        self._queue.task_done()
        return ret

    def power_on(self):
        self._pub.send('power_on')
        time.sleep(1)

    def power_off(self):
        self._pub.send('power_off')
        time.sleep(1)

    def get_angle_ranges(self):
        """関節ごとの角度の最大値と最小値を取得
        """
        res = {}
        for j in JOINTS:
            j_min = self._send(f'get_joint_min_angle,{j}')
            j_max = self._send(f'get_joint_max_angle,{j}')
            res[j] = {'min': int(j_min), 'max': int(j_max)}

        return res

    def get_angles(self):
        res = self._send('get_angles')
        return [float(val) for val in res]
