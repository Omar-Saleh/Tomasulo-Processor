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
		n = self.head - 1
		p = len(self.buffer)
		mod = (n%p + p) % p
		check = self.head == 0 and self.tail == 0
		# print(self.head, self.tail, check)
		# print((self.head % len(self.buffer)) == ((self.tail) % len(self.buffer)) and not check)
		# print("---")
		return (self.head % len(self.buffer)) == ((self.tail) % len(self.buffer)) and not check

	def issue(self):
		self.head += 1

	def peek(self):
		return self.buffer[self.head % len(self.buffer)]



		
