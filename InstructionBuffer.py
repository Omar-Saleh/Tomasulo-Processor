class InstructionBuffer(object):
	"""docstring for insturctionBuffer"""
	def __init__(self, size):
		self.buffer = [None]*size
		self.head = 0
		self.tail = 0

	def insert(self,instruction):
		self.buffer[self.tail%len(self.buffer)] = instruction
		self.tail+=1

	def isFull(self):
		return self.head-1 == self.tail

	def issue(self):
		self.head += 1

	def peek(self):
		return self.buffer[self.head]



		
