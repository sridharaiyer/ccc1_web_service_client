from xmlbase import XMLBase


class Workfile(XMLBase):
    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))


class EstimatePrintImage(XMLBase):

    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))


class UnrelatedPriorDamage(XMLBase):

    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))


class RelatedPriorDamagereport(XMLBase):

    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))


class DigitalImage(XMLBase):

    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))


class StatusChange(XMLBase):

    def __init__(self):
        self.clsname = self.__class__.__name__

    @classmethod
    def from_kwargs(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    def __repr__(self):
        return('Classname: {}, Env: {}, Est_Type: {}, Path: {}'.format(self.clsname, self.env, self.est, self.path))

    def create_xml(self):
        print('Preparing the {} XML file'.format(self.clsname))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))
