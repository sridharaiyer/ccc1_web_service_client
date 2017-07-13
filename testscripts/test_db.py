import cx_Oracle

with cx_Oracle.connect(user="EQAUSER", password="CQ*82012", dsn='CFBLQA.cbqbxxqqjewq.us-east-1.rds.amazonaws.com:1521/CFBLQA') as conn:

    cursor = conn.cursor()

    cursor.execute("select * from CLAIM_FOLDER where CUST_CLM_REF_ID = 'eqa03312017164119'")

    cols = {}
    for col, desc in enumerate(cursor.description):
        cols[desc[0]] = col

    for result in cursor:
        print(result[cols['CLM_FOLDER_STATUS']])
