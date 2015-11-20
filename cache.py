import math
class cache(object):

	"""docstring for cache"""

	
	def __init__(self, size , length , associativity , cycle_time ,writing_policy,parent ):
		#super(cache, self).__init__()
		#self.arg = arg

		self.index = (int) (math.log(associativity,2))
		
		self.offset = (int) (math.log(length,2))
		self.tag = 16-(self.index + self.offset)
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

#testing
#a = cache(4,4,4,4,"mo",None)
#b = cache(4,4,4,4,"ahmed",a)
#print(b.parent)
#



