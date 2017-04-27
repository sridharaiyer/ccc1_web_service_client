from abc import ABCMeta, abstractmethod


class Section(metaclass=ABCMeta):
    """docstring for Section"""
    @abstractmethod
    def describe(self):
        pass


class PersonalSection(Section):
    def describe():
        print('Personal Section')


class AlbumSection(Section):
    def describe():
        print('Personal Section')


class PatentSection(Section):
    def describe():
        print('Patent Section')


class PublicationSection(Section):
    def describe():
        print('Publication Section')


class Profile(metaclass=ABCMeta):
    """docstring for Profile"""

    def __init__(self):
        self.sections = []
        self.create_profile()

    @abstractmethod
    def create_profile():
        pass

    def getSections(self):
        return self.sections

    def addSection(self, section):
        self.sections.append(section)


class linkedin(Profile):
    def create_profile(self):
        self.addSection(PersonalSection())
        self.addSection(PatentSection())
        self.addSection(PublicationSection())


class facebook(Profile):
    def create_profile(self):
        self.addSection(PersonalSection())
        self.addSection(AlbumSection())


if __name__ == '__main__':
    profile_type = input('Which profile you\'d like to create? [facebook,linkedin]: ')
    profile = eval(profile_type.lower())()
    print('Creating profile: {}'.format(type(profile).__name__))
    print('Profile has sections - ', [section.describe() for section in profile.getSections()])
