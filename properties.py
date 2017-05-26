from box import Box
import json


class BoxLoad(object):
    """docstring for BoxLoad"""

    def __init__(self, properties, env='awsqa'):
        self.properties = None
        with open(properties, 'r') as f:
            self.properties = Box(json.load(f))


class Properties(object):
    __shared_state = {
        "ui": BoxLoad('properties_ui.json'),
        "db": BoxLoad('properties_db.json'),
        "ws": BoxLoad('properties_ws.json')
    }

    def __init__(self):
        self.__dict__ = self.__shared_state
    #     self.state = 'Init'

    # def __str__(self):
    #     return self.state


if __name__ == '__main__':
    p = Properties()
    print(p.ui.properties.awsqa.portal)
