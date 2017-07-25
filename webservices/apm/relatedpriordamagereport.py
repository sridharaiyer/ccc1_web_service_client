from xmlbase import XMLBase


class RelatedPriorDamagereport(XMLBase):

    def __init__(self, **params):
        super().__init__(**params)

    def edit_xml(self):
        super().edit_xml()
        super().edit_descriptor()
        super().edit_reference()

    def verify_db(self):
        print('Verifying the DB after posting the {} {} XML file'.format(self.est, self._type))

        sqls = (
            """SELECT * FROM CLAIM_FOLDER_DETAIL WHERE DL_CLM_FOLDER_ID IN (SELECT DL_CLM_FOLDER_ID FROM CLAIM_FOLDER WHERE CUST_CLM_REF_ID='{}') AND CLM_FOLDER_MATCH_FILE_TYP = '52' AND EST_LINE_IND = '{}'""",
            """SELECT * FROM BILLING_MESSAGE WHERE CLAIM_REF_ID='{}' AND MATCH_FILE_TYP = '52' AND EST_IND = '{}'"""
        )

        for sql in sqls:
            self.cf.wait_until_exists(sql.format(self.claimid, self.est))
