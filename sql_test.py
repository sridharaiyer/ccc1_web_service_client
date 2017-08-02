
claimid = '123'
est = 'E01'

match_file_type = {
    'Workfile': '2',
    'DigitalImage': '3',
    'EstimatePrintImage': '4',
    'RelatedPriorDamagereport': '52',
    'UnrelatedPriorDamage': '6',
}
sqls = (
    """SELECT * FROM CLAIM_FOLDER_DETAIL WHERE DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='{}') AND CLM_FOLDER_MATCH_FILE_TYP = '{}' AND EST_LINE_IND = '{}'""",
    """SELECT * FROM BILLING_MESSAGE WHERE CLAIM_REF_ID='{}' AND MATCH_FILE_TYP = '{}' AND EST_IND = '{}'"""
)

for ftype, value in match_file_type.items():
    for sql in sqls:
        print(sql.format(claimid, value, est))