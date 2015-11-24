import math
class Cache(object):

	"""docstring for cache"""

	
	def __init__(self, size, length, associativity, cycle_time, writing_policy,parent ):
		#super(cache, self).__init__()
		#self.arg = arg

		self.index = int(math.log(size / (length * associativity),2))
		
		self.offset = int(math.log(length,2))
		self.tag = 16 - (self.index + self.offset)
		self.num_of_sets = int( size / (length * associativity))
		self.set_size = associativity
		self.writing_policy = writing_policy
		#self.hit_cycle_time = hit_cycle_time
		#self.miss_cycle_time = miss_cycle_time
		self.cycle_time = cycle_time
		self.entries = [] # al mafrod tb2a array of class entry
		self.hits = 0
		self.misses = 0
		for i in range(self.num_of_sets):
			self.entries.append({})
		self.child = None
		self.parent = None
		self.parent = parent
		if(parent != None):
			parent.child = self
		
		print(self.num_of_sets)

	def hit_ratio(self):
		return (self.hits / (self.hits + self.misses))*100

	def __repr__(self):
		return "Index Bits: %s Offset Bits: %s Tag Bits: %s" % (self.index , self.offset , self.tag)

#testing

#a = Cache(2048,8,4,4,"wb",None)
#b = cache(4,4,4,4,"ahmed",a)
#print(b.parent)
#
# print(a) 
# mask = 0
# for i in range(1 , a.index + 1):
# 	mask |= (1 << (16 - (a.tag + i)))
# print(bin(mask))