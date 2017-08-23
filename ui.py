from webdriverwrapper import Firefox


# class Verify(object):
# 	"""docstring for Verify"""
# 	def __init__(self, arg):
# 		super(Verify, self).__init__()
# 		self.arg = arg


driver = Firefox()
driver.get('http://qa00.aws.mycccportal.com')
driver.get_elm(name='loginForm').fill_out_and_submit({
    'USERNAME': 'chase@apm1',
    'PASSWORD': 'Password1'
})
driver.wait_for_element_show(name='qsClaimReferenceId').send_keys('eqa20170821114503')
# eqa20170821114503
driver.get_elm(name='btnCFQuickSearch').click()
driver.wait_for_element_show(xpath='//a[text()="eqa20170821114503"]').click()
# driver.wait_for_element_show(xpath='//span[contains(.,"Documents for Review ")]/../following-sibling::td[contains(.,"S02")]')

driver.quit()
