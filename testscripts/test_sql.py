import sys
sys.path.append('..')

from db import DB

sql = """
SELECT FROM_CUST_ALIAS AS ADJCODE FROM
(
SELECT FROM_CUST_ALIAS FROM CUSTOMER_RELATIONSHIP
WHERE FROM_DL_CUST_ID =
(
SELECT DL_CUST_ID FROM CUSTOMER_REGISTERED WHERE CUST_OFCE_ID = '{}' AND CORP_OFCE_DL_CUST_ID =
(SELECT DL_CUST_ID FROM CUSTOMER_REGISTERED WHERE CUST_OFCE_ID = '{}' AND CUST_OFCE_TYP = 'HO')
)
AND ALIAS_TYP_CD = 'ADJ'
AND FROM_CUST_ALIAS NOT LIKE 'xxx%'
ORDER BY DBMS_RANDOM.VALUE
)
WHERE ROWNUM = 1
"""

db = DB('awsqa')
newsql = sql.format('APMC', 'APM1')
print(db.claimfolder.execute(newsql)[0][0])
print(db.claimfolder.execute(newsql)[0][0])
# print(adjustercode)
