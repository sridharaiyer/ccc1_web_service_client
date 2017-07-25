import cx_Oracle
from properties import Properties
import pdb


rec_exists = """SELECT CASE WHEN EXISTS ({})
                THEN 'TRUE' ELSE 'FALSE'
                END AS REC_EXISTS
                FROM DUAL"""


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
        self.timeout = 1200

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
    sql = "select * from CLAIM_FOLDER where COMPRSD_CUST_CLM_REF_ID = 'eqa0702201722475537'"
    # print(db.claimfolder.execute(sql)[0][0])
    # assert db.claimfolder.rowcount == 1
    # assert db.claimfolder.get('CLM_FOLDER_STATUS') == 'OPEN'
    # print(db.claimfolder.result[0][0])
