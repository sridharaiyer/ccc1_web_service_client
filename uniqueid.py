import datetime


class UniqueID(object):

    dt = datetime.datetime.now()

    @staticmethod
    def random_id(prefix='eqa'):
        return prefix + UniqueID.dt.strftime('%Y%m%d%H%M%S')


if __name__ == '__main__':
    print(UniqueID.random_id())
