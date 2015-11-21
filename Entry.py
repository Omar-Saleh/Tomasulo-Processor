class Entry(object):
	"""docstring for Entry"""

	def __init__(self, valid_bit, dirty_bit,address , data):
		self.valid_bit = valid_bit 
		self.dirty_bit = dirty_bit
		self.data = data
		self.address = address
		self.data = None
