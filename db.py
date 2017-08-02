import cx_Oracle
from properties import Properties
import pdb
import time


rec_exists = """SELECT CASE WHEN EXISTS ({})
                THEN 'TRUE' ELSE 'FALSE'
                END AS REC_EXISTS
                FROM DUAL"""


class NoRecordException(Exception):

    def __init__(self, query, timeoutmins):
        self.query = query
        self.timeoutmins = timeoutmins

    def __str__(self):
        return ('No result found for {} even after {} mins'.format(self.query, self.timeoutmins))


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class _DB(metaclass=Singleton):

    def __init__(self, **params):
        self.dsn = '{}:{}/{}'.format(params['host'],
                                     params['port'],
                                     params['service_name'])

        self.conn = cx_Oracle.connect(user=params['user'],
                                      password=params['password'],
                                      dsn=self.dsn)
        self.cursor = self.conn.cursor()
        self.cols = {}
        self.timeoutmins = 20

    def execute(self, query):
        self.cols.clear()
        self.cursor.execute(query)
        self.result = self.cursor.fetchall()
        self._rowcount = self.cursor.rowcount
        for col, desc in enumerate(self.cursor.description):
            self.cols[desc[0]] = col
        return self.result

    def _check_exists(self, query):
        exists = self.execute(rec_exists.format(query))[0][0]
        if exists.upper() == 'TRUE':
            return True
        else:
            return False

    def wait_until_exists(self, query):
        timeout = time.time() + self.timeoutmins * 60
        a = 1
        while True:
            print('Query attempt {}'.format(a))
            if self._check_exists(query):
                break
            elif time.time() > timeout:
                raise NoRecordException(query, self.timeoutmins)
            a += 1

            time.sleep(5)

    @property
    def rowcount(self):
        return self._rowcount

    def get(self, col):
        return(self.result[0][self.cols[col]])

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DB(metaclass=Singleton):

    def __init__(self, env):
        self._map = {}
        self._env = env

        for db, dbparams in Properties(env).db.items():
            self._map[db] = {'params': dbparams, 'existing': None}

    def __getattr__(self, dbname):
        if dbname in self._map:
            db = self._map[dbname]
            dbparams = db.get('params')
            dbexisting = db.get('existing')

            if dbexisting:
                return dbexisting

            if dbparams is None:
                raise AttributeError(
                    'Database {} is not registered in the property file'.format(dbname))
            elif dbexisting is None:
                print(
                    'Establishing DB connection to ({}) - {} DB'.format(self._env, dbname))
                dbobject = _DB(**dbparams)
                self._map[dbname]['existing'] = dbobject
                print('Connection to ({}) - {} DB successful'.format(self._env, dbname))
                return dbobject


if __name__ == '__main__':
    db = DB('awsqa')
    sql = """SELECT * FROM CLAIM_FOLDER_DETAIL WHERE DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='eqa20170802113813') AND CLM_FOLDER_MATCH_FILE_TYP = '2' AND EST_LINE_IND = 'E01'"""
    db.claimfolder.wait_until_exists(sql)
    # assert db.claimfolder.rowcount == 1
    # assert db.claimfolder.get('CLM_FOLDER_STATUS') == 'OPEN'
    # print(db.claimfolder.result[0][0])
