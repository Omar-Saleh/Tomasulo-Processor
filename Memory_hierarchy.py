class Memory_hierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, cache_l1):
		super(Memory-hierarchy, self).__init__()
		self.arg = arg
		self.cache_l1 = cache_l1


	def search(address,cache):
		tag_bits = cache.tag
		index_bits = cache.index
		offset_bits = cache.offset

		tag = address[:tag_bits]
		index = address[tag_bits:tag_bits+index_bits]
		offset = address[-offset_bits:]
		
		for i in range(cache.entries):
			if(i.tag == tag):
				return cache.cycle_time

		if(cache.child != None):
			return cache.cycle_time + search(address,cache.child)
		else:
			return cache.cycle_time #+ main memory cycle time 
			
	#def search(address , cache):
		

