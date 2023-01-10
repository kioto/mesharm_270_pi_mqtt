"""meshArm 270 PIコントローラ
"""
import sys
import PySimpleGUI as sg
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('../common')))
from config import Config
from comm import ClientComm

DEFAULT_CONFIG_FILE = 'config.yaml'


JOINT_RANGE_J1_MIN = -30
JOINT_RANGE_J1_MAX = 159
JOINT_RANGE_J2_MIN = -84
JOINT_RANGE_J2_MAX = 90
JOINT_RANGE_J3_MIN = -178
JOINT_RANGE_J3_MAX = 45
JOINT_RANGE_J4_MIN = -160
JOINT_RANGE_J4_MAX = 159
JOINT_RANGE_J5_MIN = -99
JOINT_RANGE_J5_MAX = 100
JOINT_RANGE_J6_MIN = -180
JOINT_RANGE_J6_MAX = 178

HOME = (56, -10, 29, -14, 38, 170)

# send_angles,56,-10,29,-14,38,170,20
# send_angles,60,-80,45,0,45,0,20


class ClientGui(object):

    def __init__(self, config):
        self._config = config
        self._comm = ClientComm(self._config)
        sg.theme('Dark Blue 3')

    def run(self):
        self._init_client()
        self._setup_window()

    def _init_client(self):
        #self._comm.power_on()
        angles = self._comm.get_angles()
        self._j1 = angles[0]
        self._j2 = angles[1]
        self._j3 = angles[2]
        self._j4 = angles[3]
        self._j5 = angles[4]
        self._j6 = angles[5]

    def _setup_window(self):
        layout = [
            [
                sg.Text('J1:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J1_MIN, JOINT_RANGE_J1_MAX),
                          default_value=self._j1,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J1')
            ],
            [
                sg.Text('J2:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J2_MIN, JOINT_RANGE_J2_MAX),
                          default_value=self._j2,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J2')
            ],
            [
                sg.Text('J3:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J3_MIN, JOINT_RANGE_J3_MAX),
                          default_value=self._j3,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J3')
            ],
            [
                sg.Text('J4:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J4_MIN, JOINT_RANGE_J4_MAX),
                          default_value=self._j4,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J4')
            ],
            [
                sg.Text('J5:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J5_MIN, JOINT_RANGE_J5_MAX),
                          default_value=self._j5,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J5')],
            [
                sg.Text('J6:', size=(2, 0)),
                sg.Slider(range=(JOINT_RANGE_J6_MIN, JOINT_RANGE_J6_MAX),
                          default_value=self._j6,
                          orientation='h',
                          size=(34, 15),
                          enable_events=True,
                          key='J6')
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Button('Quit', key='quit')
            ]
        ]
        window = sg.Window('mashArm 270 PI controller',
                           layout,
                           size=(310, 270))

        while True:
            event, values = window.read()
            if event == 'quit':
                exit()
            elif event in ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', ]:
                print(event, values[event])


if __name__ == '__main__':
    config_file = DEFAULT_CONFIG_FILE
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]

    config = Config(config_file)
    client = ClientGui(config)
    client.run()
