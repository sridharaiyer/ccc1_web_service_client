from box import Box
import json

prop_dict = {
    'ui': 'properties_ui.json',
    'db': 'properties_db.json',
    'ws': 'properties_ws.json'
}


class BoxLoad(object):
    """docstring for BoxLoad"""

    def __init__(self, file, env):
        with open(file, 'r') as f:
            self.properties = Box(json.load(f)[env])


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class Properties(metaclass=Singleton):
    def __init__(self, env):
        self.env = env
        self.ui = BoxLoad(prop_dict['ui'], env).properties
        self.db = BoxLoad(prop_dict['db'], env).properties
        self.ws = BoxLoad(prop_dict['ws'], env).properties


if __name__ == '__main__':
    p = Properties('awsqa')
    print(p.ws.StatusChange)
