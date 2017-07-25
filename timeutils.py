import datetime
import pytz
from dateutil.relativedelta import relativedelta


class Time(object):
    now = datetime.datetime.now(pytz.timezone('US/Central'))
    iso = now.isoformat()
    ymdhms = now.strftime('%Y-%m-%dT%H:%M:%S')
    ymd = now.strftime('%Y-%m-%d')

    utc = datetime.datetime.utcnow()
    utc = utc.replace(tzinfo=pytz.timezone('GMT')).isoformat()
    zulu = utc + 'Z'


if __name__ == '__main__':
    time = Time()
    print('Now: ' + str(time.now))
    print(time.utc)
