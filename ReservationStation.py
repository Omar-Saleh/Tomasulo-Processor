class ReservationStation(object):
	"""docstring for ReservationStation"""
	def __init__(self, name , cycles):
		self.name = name
		self.busy = False
		self.op = None
		self.readySource1 = None
		self.readySource2 = None
		self.notReadySource1 = None
		self.notReadySource2 = None
		self.dest = None
		self.address = None
		self.branchOffset = None
		self.currentCycles = cycles
		self.cycles = cycles
	def check(self):
		return self.busy

	def reserve(self, op , readySource1 , readySource2 , notReadySource1 , notReadySource2 , dest , address, branchOffset):
		self.op = op
		self.readySource1 = readySource1
		self.readySource2 = readySource2
		self.notReadySource1 = notReadySource1
		self.notReadySource2 = notReadySource2
		self.dest = dest
		self.address = address
		self.branchOffset = branchOffset
		self.busy = True

	def execute(self):
		self.currentCycles -= 1

	def flush(self):
		self.busy = False
		self.op = None
		self.readySource1 = None
		self.readySource2 = None
		self.notReadySource1 = None
		self.notReadySource2 = None
		self.dest = None
		self.address = None
		self.branchOffset = None
		self.currentCycles = self.cycles

