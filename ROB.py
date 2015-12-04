from ROB_Entry import *

class ROB(object):
	"""docstring fos ROB"""
	def __init__(self, size):

		self.ROB_Entries = [None]*size
		self.head = 0
		self.tail = 0
		self.size = size

	def add(self,rtype,dest ,value):
		self.ROB_Entries[self.tail % self.size] = ROB_Entry(rtype,dest,value)
		self.tail += 1
		return self.tail - 1
	
	def update(self, value,index):
		self.ROB_Entries[index % self.size].value = value
		self.ROB_Entries[index % self.size].ready = True

	def commit(self):
		if(self.ROB_Entries[self.head % self.size].ready):
			self.ROB_Entries[self.head % self.size] = None
			self.head += 1


	def flush(self):
		self.head = 0
		self.tail = 0
		self.ROB_Entries = [None] *self.size

	def isFull(self):
		check = self.head == self.tail and self.ROB_Entries[self.head % self.size] == None
		# print(self.head, self.tail, check)
		# print((self.head % len(self.buffer)) == ((self.tail) % len(self.buffer)) and not check)
		# print("---")
		# print((self.head % self.size) == ((self.tail) % self.size) and not check)
		return (self.head % self.size) == ((self.tail) % self.size) and not check