import cx_Oracle

conn = cx_Oracle.connect(user="EQAUSER", password="CQ*82012", dsn='CFBLQA.cbqbxxqqjewq.us-east-1.rds.amazonaws.com:1521/CFBLQA')

cursor = conn.cursor()

cursor.execute("select * from CLAIM_FOLDER where CUST_CLM_REF_ID = 'eqa03312017164119'")
# print(cursor.fetchall())
# print('{}'.format([i[0] for i in cursor.description]))

cols={}
for col, desc in enumerate(cursor.description):
    cols[desc[0]] = col

for result in cursor:
    print (result[cols['CLM_FOLDER_STATUS']])