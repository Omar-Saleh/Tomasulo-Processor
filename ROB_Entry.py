class ROB_Entry(object):
	"""docstring fos ROB_Entry"""
	def __init__(self, rtype , dest , value ):
		self.type = rtype
		self.dest = dest 
		self.value = value
		self.ready = False
		