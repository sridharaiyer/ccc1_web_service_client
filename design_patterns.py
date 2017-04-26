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
