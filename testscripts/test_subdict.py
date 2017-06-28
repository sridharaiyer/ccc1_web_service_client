big_dict = {
    'fruit': 'apple',
    'veggie': 'cabbage',
    'greens': 'spinach',
    'protein': 'tofu',
    'carbs': 'bread'
}


class SuperClass(object):
    """docstring for SuperClass"""

    def __init__(self, **params):
        self.fruit = params['fruit']
        self.veggie = params['veggie']


class ChildClass(SuperClass):
    """docstring for ChildClass"""

    def __init__(self, **params):
        super(ChildClass, self).__init__(fruit=params.pop('fruit'),
                                         veggie=params.pop('veggie'))
        self.greens = params['greens']
        self.protein = params['protein']
        self.carbs = params['carbs']


if __name__ == '__main__':
    obj = ChildClass(**big_dict)
    print(obj.fruit)
