from abc import ABCMeta, abstractmethod


class Trip(metaclass=ABCMeta):
    """docstring for Trip"""

    @abstractmethod
    def set_transport(self):
        pass

    @abstractmethod
    def day1(self):
        pass

    @abstractmethod
    def day2(self):
        pass

    @abstractmethod
    def day3(self):
        pass

    @abstractmethod
    def return_home(self):
        pass

    def itenerary(self):
        self.set_transport()
        self.day1()
        self.day2()
        self.day3()
        self.return_home()


class VeniceTrip(Trip):
    """docstring for VeniceTrip"""

    def set_transport(self):
        print('Take a boat on the Grand Canal')

    def day1(self):
        print('Visit St Mark\'s Bascilla on St Mark\'s Square')

    def day2(self):
        print('Appreciate Doge Palace')

    def day3(self):
        print('Enjoy food near Rialto Bridge')

    def return_home(self):
        print('Get souvenirs for friends and family and board flight from Venice Airport')


class MiamiTrip(Trip):
    """docstring for VeniceTrip"""

    def set_transport(self):
        print('Walk on beach')

    def day1(self):
        print('Enjoy the marine life on Banana Reef')

    def day2(self):
        print('Do water sports and snorkeling')

    def day3(self):
        print('Relax on the beach and enjoy the sun')

    def return_home(self):
        print('Get souvenirs for friends and family and board flight from Miami Airport')


class TravelAgency(object):
    def arrange_trip(self):
        choice = input('What kind of place you want to visit, historical or beach: ')
        if choice == u'historical':
            self.trip = VeniceTrip()
            self.itenerary = self.trip.itenerary()

        if choice == u'beach':
            self.trip = MiamiTrip()
            self.itenerary = self.trip.itenerary()


if __name__ == '__main__':
    TravelAgency().arrange_trip()
