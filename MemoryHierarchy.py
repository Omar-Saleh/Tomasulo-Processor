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

	# 	Binary Conversion 
	#	tag = address[:tag_bits]
	#	index = address[tag_bits:tag_bits+index_bits]
	#	offset = address[-offset_bits:]

		""" Using Numbers instead of binary the mask only sets
		the tag bits for the address_tag and the index bits for the index_tag """
		mask = 0
		for i in range(1 , a.tag_bits + 1):
			mask |= (1 << (16 - i))
		address_tag = address & mask
		mask = 0
		for i in range(1 , a.index_bits + 1):
			mask |= (1 << (16 - (a.tag_bits + i)))
		address_index = address & mask
		# Checking with the address_index and address_tag for the entry
		if address_tag in cache.entries[address_index]:
			m.update(entries[address_index][address_tag] , cache.parent)
		if(cache.child != None):
			search(address, cache.chid)
		else:
		# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
			e = Entry()
			m.update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		
# Update should update all the cache blocks above the level where the entry was found
	def update(self, entry, cache):
		pass


# Write Back should write down to a cache/main memory if there was no empty space to write and the entry was marked as dirty
	def write_back(self, entry, cache):
		pass

a = Cache(4,4,4,4,"wb",None)
m = MemoryHierarchy(a)
m.search("01010101", a)