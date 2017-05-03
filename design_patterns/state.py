class ComputerState(object):
    name = 'state'
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print('Current state: {}, switched to new state {}'.format(self, state.name))
            self.__class__ = state
        else:
            print('Current state: {} switching to {} not possible'.format(self, state.name))

    def __str__(self):
        return self.name


class Off(ComputerState):
    name = 'Off'
    allowed = ['On']


class On(ComputerState):
    name = 'On'
    allowed = ['Off', 'Hibernate', 'Suspend']


class Hibernate(ComputerState):
    name = 'Hibernate'
    allowed = ['On']


class Suspend(ComputerState):
    name = 'Suspend'
    allowed = ['On']


class Computer(object):
    """docstring for Computer"""

    def __init__(self, model='MacBook Pro'):
        self.model = model
        self.state = Off()

    def change(self, state):
        self.state.switch(state)


if __name__ == "__main__":
    comp = Computer()
    comp.change(On)
    comp.change(Off)
    comp.change(Hibernate)
    comp.change(On)
    comp.change(Hibernate)
    comp.change(On)
    comp.change(Suspend)
    comp.change(Off)
    comp.change(On)
    comp.change(Off)
