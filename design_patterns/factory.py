from abc import ABCMeta, abstractmethod
import random


class Section(metaclass=ABCMeta):
    """docstring for Section"""
    @abstractmethod
    def describe(self):
        pass


class PersonalSection(Section):

    def describe(self):
        print('Personal Section')


class AlbumSection(Section):

    def describe(self):
        print('Album Section')


class PatentSection(Section):

    def describe(self):
        print('Patent Section')


class PublicationSection(Section):

    def describe(self):
        print('Publication Section')


class Profile(metaclass=ABCMeta):
    """docstring for Profile"""

    def __init__(self):
        self.sections = []
        self.create_profile()

    @abstractmethod
    def create_profile(self):
        pass

    def getSections(self):
        return self.sections

    def addSection(self, section):
        self.sections.append(section)


class Linkedin(Profile):

    def create_profile(self):
        self.addSection(PersonalSection())
        self.addSection(PatentSection())
        self.addSection(PublicationSection())


class Facebook(Profile):

    def create_profile(self):
        self.addSection(PersonalSection())
        self.addSection(AlbumSection())


if __name__ == '__main__':
    profile = random.choice([Linkedin, Facebook])()
    print('Creating profile: {}'.format(type(profile).__name__))
    [section.describe() for section in profile.getSections()]
