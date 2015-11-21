from Entry import *
from Cache import *

class MemoryHierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, cache_l1):
		self.cache_l1 = cache_l1


	def search(self, address, cache):
		tag_bits = cache.tag
		index_bits = cache.index
		offset_bits = cache.offset

		tag = address[:tag_bits]
		index = address[tag_bits:tag_bits+index_bits]
		offset = address[-offset_bits:]
		print(tag, index , offset)
		for i in range(len(cache.entries)):
			if tag in cache.entries[i]:
				m.update(entries[i][tag] , cache.parent)
		if(cache.child != None):
			search(address, cache.chid)
		else:
		# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
			e = Entry()
			m.update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		

	def update(self, entry, cache):
		pass

	def write_back(self, entry, cache):
		pass

a = Cache(4,4,4,4,"wb",None)
m = MemoryHierarchy(a)
m.search("01010101", a)