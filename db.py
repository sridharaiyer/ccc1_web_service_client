import cx_Oracle
from properties import Properties
import pdb


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

    def execute(self, query):
        self.cols.clear()
        self.cursor.execute(query)
        for col, desc in enumerate(self.cursor.description):
            self.cols[desc[0]] = col

    def get(self, col):
        for result in self.cursor:
            return result[self.cols[col]]

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


class DB(object):

    def __init__(self, env):
        self._map = {}
        self._env = env

        for db, dbparams in Properties(env).db.items():
            print('Registering {} DB'.format(db))
            self._map[db] = {'params': dbparams, 'existing': None}

    def __getattr__(self, dbname):
        if dbname in self._map:
            db = self._map[dbname]
            dbparams = db.get('params')
            dbexisting = db.get('existing')

            if dbexisting:
                print('Returning {} object - {}'.format(dbname, dbexisting))
                return dbexisting

            if dbparams is None:
                raise AttributeError(
                    'Database {} is not registered in the property file'.format(dbname))
            elif dbexisting is None:
                print(
                    'Establishing DB connection to ({}) - {} DB'.format(self._env, dbname))
                dbobject = _DB(**dbparams)
                self._map[dbname]['existing'] = dbobject
                print('Connection to ({}) - {} DB successful'.format(self._env, db))
                return dbobject


if __name__ == '__main__':
    print('DB object 1')
    db1 = DB('awsqa')
    # print(db1.test)
    db1.claimfolder.execute(
        "select * from CLAIM_FOLDER where CUST_CLM_REF_ID = 'eqa03312017164119'")
    print()
    assert db1.claimfolder.get('CLM_FOLDER_STATUS') == 'OPEN'

    print('\nDB object 2')
    db2 = DB('awsqa')
    db2.claimfolder.execute(
        "select * from CLAIM_FOLDER where CUST_CLM_REF_ID = 'eqa03312017164119'")
    print()
    assert db2.claimfolder.get('CLM_FOLDER_STATUS') == 'OPEN'
