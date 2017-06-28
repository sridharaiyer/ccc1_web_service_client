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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(SourceTimeStamp=super().time_iso)
        self.xml.edit_tag(PublishTimeStamp=super().time_iso)
        self.xml.edit_tag(ClaimReferenceID=self.claimid)
        self.xml.edit_tag(SourceTimeStamp=super().time_iso)
        self.xml.edit_tag(PublishTimeStamp=super().time_iso)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(SourceTimeStamp=super().time_iso)
        self.xml.edit_tag(PublishTimeStamp=super().time_iso)

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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(SourceTimeStamp=super().time_iso)
        self.xml.edit_tag(PublishTimeStamp=super().time_iso)
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')
        self.xml.edit_tag(Password='Password1')

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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

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

    def create_xml(self):
        print('Preparing the {} XML file located in {} in the fiddler session'.format(self.clsname, self.path))

    def send_xml(self):
        print('Sending the {} XML file to endpoint'.format(self.clsname))

    def verify_db(self):
        print('Verifying the DB after posting the {} XML file'.format(self.clsname))
