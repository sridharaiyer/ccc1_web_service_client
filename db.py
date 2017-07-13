import cx_Oracle
from properties import Properties
import pdb


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class _DB(object):
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
        for db, dbparams in Properties(env).db.items():
            # if k == 'claimfolder':
            print('Establishing DB connection to ({}) - {} DB'.format(env, db))
            dbobject = _DB(**dbparams)
            print('Connection to ({}) - {} DB successful'.format(env, db))
            setattr(self, db, dbobject)


if __name__ == '__main__':
    db = DB('awsqa')
    db.claimfolder.execute("select * from CLAIM_FOLDER where CUST_CLM_REF_ID = 'eqa03312017164119'")
    assert db.claimfolder.get('CLM_FOLDER_STATUS') == 'OPEN'
