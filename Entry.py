class Entry(object):
	"""docstring for Entry"""

	def __init__(self, valid_bit, dirty_bit,address):
		self.valid_bit = valid_bit 
		self.dirty_bit = dirty_bit
		self.address = address


	def __repr__(self):
		return "Valid: %s Dirty: %s Address: %s " % (self.valid_bit, self.dirty_bit, self.address)
