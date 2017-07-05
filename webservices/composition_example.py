from datetime import datetime


class WriteFile(object):
    """docstring for WriteFile"""

    def __init__(self, filename, formatter):
        super(WriteFile, self).__init__()
        self.filename = filename
        # self.fh = open(filename, 'w')
        self.formatter = formatter()

    def __enter__(self):
        print('I am in __enter__')
        self.fh = open(self.filename, 'w')
        return self.fh

    def close(self):
        self.fh.close()

    def write(self, text):
        self.fh.write(self.formatter.format(text))
        self.fh.write('\n')

    def __exit__(self, type, value, traceback):
        print('Closing: {}'.format(self.filename))
        self.fh.close()


class CSVFormatter(object):
    """docstring for CVSWriter"""

    def __init__(self):
        self.delim = ','

    def format(self, this_list):
        new_list = []
        for elem in this_list:
            if self.delim in elem:
                new_list.append('"{0}"'.format(elem))
            else:
                new_list.append(elem)
        return self.delim.join(new_list)


class LogFormatter(object):
    """docstring for LogFormatter"""

    def format(self, this_line):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return '{0}  {1}'.format(timestamp, this_line)


# writecsv = WriteFile('tempcsv.csv', CSVFormatter)
# writecsv.write(['a', 'b', 'c,d', 'e'])
# writecsv.write(['Blue', 'Green', 'Yello:Orange', 'Pink'])

# writelogger = WriteFile('temptext.txt', LogFormatter)
# writelogger.write('This is a log message')
# writelogger.write('This is another log message')

# writecsv.close()
# writelogger.close()

with WriteFile('tempcsv.csv', CSVFormatter) as writecsv:
    writecsv.write(['a', 'b', 'c,d', 'e'])
    writecsv.write(['Blue', 'Green', 'Yello:Orange', 'Pink'])

with WriteFile('temptext.txt', LogFormatter) as writelogger:
    writelogger.write('This is a log message')
    writelogger.write('This is another log message')
