class BaseClass(object):
    @classmethod
    def get_subclass_name(cls):
        return cls.__name__

    def somemethod(self):
        print(self.get_subclass_name())


class SubClass(BaseClass):
    pass


if __name__ == '__main__':
    SubClass().somemethod()
