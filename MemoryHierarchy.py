from Entry import *
from Cache import *

class MemoryHierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, cache_l1):
		self.cache_l1 = cache_l1


	def search(address, cache):
		tag_bits = cache.tag
		index_bits = cache.index
		offset_bits = cache.offset

		tag = address[:tag_bits]
		index = address[tag_bits:tag_bits+index_bits]
		offset = address[-offset_bits:]
		
		for i in range(len(cache.entries)):
			if entries[i][tag]:
				update(entries[i][tag] , cache.parent)
		if(cache.child != None):
			search(address, cache.chid)
		else:
		# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
			e = Entry()
			update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		

	def update(entry, cache):
		pass