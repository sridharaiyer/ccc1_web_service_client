import json

prop_dict = {
    'ui': 'properties_ui.json',
    'db': 'properties_db.json',
    'ws': 'properties_ws.json'
}


class PropertiesLoad(object):
    """docstring for PropertiesLoad"""

    def __init__(self, file, env):
        with open(file, 'r') as f:
            self.properties = json.load(f)[env]


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class Properties(metaclass=Singleton):

    def __init__(self, env):
        self.env = env
        self.ui = PropertiesLoad(prop_dict['ui'], env).properties
        self.db = PropertiesLoad(prop_dict['db'], env).properties
        self.ws = PropertiesLoad(prop_dict['ws'], env).properties


if __name__ == '__main__':
    p = Properties('awsqa')
    print(p.ws['StatusChange'])
