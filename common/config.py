"""設定データクラス
"""
import yaml


class Config(object):
    """Configuration data
    """

    def __init__(self, config_file):
        conf_obj = None
        with open(config_file, 'r') as f:
            conf_obj = yaml.safe_load(f)

        # broker information
        broker = conf_obj.get('broker')
        if broker is None:
            raise ValueError('ERROR: Config: undefined broker')
        self.host = broker.get('host')
        self.port = broker.get('port')

        # topic information
        topic = conf_obj.get('topic')
        if topic is None:
            raise ValueError('ERROR: Config: undefined topic')
        self.topic_command = topic.get('command')
        self.topic_response = topic.get('response')
