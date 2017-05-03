from abc import ABCMeta, abstractmethod


class PizzaFactory(metaclass=ABCMeta):
    @abstractmethod
    def createvegpizza(self):
        pass

    @abstractmethod
    def createnonvegpizza(self):
        pass


class VegPizza(metaclass=ABCMeta):
    @abstractmethod
    def prepare(self, VegPizza):
        pass


class NonVegPizza(metaclass=ABCMeta):
    @abstractmethod
    def serve(self, VegPizza):
        pass


class DeluxeVeggiePizza(VegPizza):
    def prepare(self):
        print('Prepare - {}'.format(type(self).__name__))


class ChickenPizza(NonVegPizza):
    def serve(self, VegPizza):
        print('Serving {} on top of {}'.format(type(self).__name__, type(VegPizza).__name__))


class MexicanVeggiePizza(VegPizza):
    def prepare(self):
        print('Prepare - {}'.format(type(self).__name__))


class HamPizza(NonVegPizza):
    def serve(self, VegPizza):
        print('Serving {} on top of {}'.format(type(self).__name__, type(VegPizza).__name__))


class IndianPizzaFactory(PizzaFactory):
    def createvegpizza(self):
        return DeluxeVeggiePizza()

    def createnonvegpizza(self):
        return ChickenPizza()


class USPizzaFactory(object):
    def createvegpizza(self):
        return MexicanVeggiePizza()

    def createnonvegpizza(self):
        return HamPizza()


class PizzaStore(object):
    """docstring for PizzaStore"""

    def __init__(self):
        pass

    def make_pizzas(self):
        for factory in [IndianPizzaFactory(), USPizzaFactory()]:
            self.factory = factory
            self.vegpizza = self.factory.createvegpizza()
            self.vegpizza.prepare()
            self.nonvegpizza = self.factory.createnonvegpizza()
            self.nonvegpizza.serve(self.vegpizza)


if __name__ == '__main__':
    PizzaStore().make_pizzas()
