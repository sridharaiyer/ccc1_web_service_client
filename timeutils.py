import datetime
import pytz


class Time(object):
    now = datetime.datetime.now(pytz.timezone('US/Central'))
    iso = now.isoformat()
    ymdhms = now.strftime('%Y-%m-%dT%H:%M:%S')
    ymd = now.strftime('%Y-%m-%d')

    utc = datetime.datetime.utcnow()
    utc = utc.replace(tzinfo=pytz.timezone('US/Central')).isoformat()
    zulu = utc + 'Z'


if __name__ == '__main__':
    time = Time()
    print(time.now)
