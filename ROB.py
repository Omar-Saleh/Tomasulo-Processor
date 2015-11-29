from ROB_Entry import *

class ROB(object):
	"""docstring fos ROB"""
	def __init__(self, size):

		self.ROB_Entries = [None]*size
		self.head =0
		self.tail =0
		self.size = size

	def add(self,rtype,dest ,value):
		self.ROB_Entries[self.tail % self.size] = ROB_Entry(rtype,dest,value)
		self.tail += 1
	
	def update(self, value,index):
		self.ROB_Entries[index].value = value
		self.ROB_Entries[index].ready = True

	def commit(self):
		if(self.ROB_Entries[self.head].ready):
			self.head += 1


	def flush(self):
		self.head = 0
		self.tail = 0
		self.ROB_Entries = [None] *self.size