class InstructionBuffer(object):
	"""docstring for insturctionBuffer"""
	def __init__(self, size):
		self.buffer = [None]*size
		self.head = 0
		self.tail = 0

	def insert(self,instruction):
		self.buffer[self.tail % len(self.buffer)] = instruction
		self.tail += 1

	def isFull(self):
		check = self.head == self.tail and self.buffer[self.head % len(self.buffer)] == None
		# print(self.head, self.tail, check)
		# print((self.head % len(self.buffer)) == ((self.tail) % len(self.buffer)) and not check)
		# print("---")
		return (self.head % len(self.buffer)) == ((self.tail) % len(self.buffer)) and not check

	def issue(self):
		self.buffer[self.head % len(self.buffer)] = None
		self.head += 1

	def peek(self):
		return self.buffer[self.head % len(self.buffer)]



		
