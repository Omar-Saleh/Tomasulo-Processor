class RegisterStatus(object):
	"""docstring for RegisterStatus"""
	def __init__(self):
		self.registers = {}
		for i in range(31):
			self.registers["r"+str(i)] = None

	def flush(self):
		for i in range(31):
			self.registers["r" + str(i)] = None


