import math
class Cache(object):

	"""docstring for cache"""

	
	def __init__(self, size , length , associativity , cycle_time ,writing_policy,parent ):
		#super(cache, self).__init__()
		#self.arg = arg

		self.index = int(math.log(size / (length * associativity),2))
		
		self.offset = int(math.log(length,2))
		self.tag = 16 - (self.index + self.offset)
		self.no_of_sets = associativity
		self.writing_policy = writing_policy
		self.cycle_time = cycle_time

		self.entries = [] # al mafrod tb2a array of class entry

		for i in range(self.no_of_sets):
			self.entries.append({})
		self.child = None
		self.parent = None
		self.parent = parent
		if(parent != None):
			parent.child = self

	def __repr__(self):
		return "Index Bits: %s Offset Bits: %s Tag Bits: %s" % (self.index , self.offset , self.tag)

#testing
a = Cache(2048,8,4,4,"wb",None)
#b = cache(4,4,4,4,"ahmed",a)
#print(b.parent)
#
print(a) 
mask = 0
for i in range(1 , a.index + 1):
	mask |= (1 << (16 - (a.tag + i)))
print(bin(mask))