import sqlite3


class Singleton(object):
    """docstring for Singleton"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


s1 = Singleton()
print('Object created: {}'.format(s1))

s2 = Singleton()
print('Object created: {}'.format(s2))


class Borg(object):
    _shared_state = {'x': '1'}
    """docstring for Borg"""
    def __new__(cls, *arg, **kwargs):
        obj = super(Borg, cls).__new__(cls, *arg, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


b1 = Borg()
b1.y = 4
b2 = Borg()
b2.z = 5

print('Borg object b1: {}'.format(b1))
print('Borg object b1 state: {}'.format(b1.__dict__))
print('Borg object b2: {}'.format(b2))
print('Borg object b2 state: {}'.format(b2.__dict__))


class MetaSingleton(type):
    _instances = {}
    """docstring for MetaSingleton"""

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db.sqlite3')
            self.cursorobj = self.connection.cursor()
        return self.cursorobj


db1 = Database().connect()
db2 = Database().connect()

print('db1 object: {}'.format(db1))
print('db2 object: {}'.format(db2))
