from webdriverwrapper import Firefox


# class Verify(object):
# 	"""docstring for Verify"""
# 	def __init__(self, arg):
# 		super(Verify, self).__init__()
# 		self.arg = arg
		


driver = Firefox()
driver.get('http://qa00.aws.mycccportal.com')
driver.get_elm(id='loginForm').fill_out_and_submit({
	'':'',
	'': ''
	})

#eqa20170821114503
driver.quit()
