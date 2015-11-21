from Entry import *
from Cache import *
import random

class MemoryHierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, filename, main_memory_access_time):
		self.i_cache = filename
		self.elapsed_time = 0
		self.main_memory = {}
		self.main_memory_access_time = main_memory_access_time

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
		for i in range(1 , cache.tag + 1):
			mask |= (1 << (16 - i))
		address_tag = address & mask
	
		mask = 0
		for i in range(1 , cache.index + 1):
			mask |= (1 << (16 - (cache.tag + i)))
		address_index = address & mask
		address_index >>= cache.offset
		# Checking with the address_index and address_tag for the entry
		print(address_index)
		print(mask)
		print(cache)
		if address_tag in cache.entries[address_index]:
			self.elapsed_time += cache.hit_cycle_time
			m.update(entries[address_index][address_tag] , cache.parent)
		if(cache.child != None):
			self.elapsed_time += cache.cycle_time
			search(address, cache.chid)
		else:
		# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
			self.elapsed_time += cache.cycle_time + self.main_memory_access_time
			e = Entry(1, 1, 512, "aa")
			m.update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		
# Update should update all the cache blocks above the level where the entry was found
	def update(self, entry, cache):
		#pass
		mask = 0
		for i in range(1 , cache.tag + 1):
			mask |= (1 << (16 - i))
		address_tag = entry.address & mask

		mask = 0
		for i in range(1 , cache.index + 1):
			mask |= (1 << (16 - (cache.tag + i)))
		address_index = entry.address & mask
		address_index >>= cache.offset

		if(len(cache.entries[address_index])== cache.set_size ):
			m.replace(entry, cache)
		else:
			cache.entries[address_index][address_tag] = entry

		if(cache.parent != None):
			self.elapsed_time += cache.cycle_time
			m.update(entry,cache.parent)


# Write Back should write down to a cache/main memory if there was no empty space to write and the entry was marked as dirty
	def replace(self, entry, cache):
		#pass
		mask = 0
		for i in range(1 , cache.tag + 1):
			mask |= (1 << (16 - i))
		address_tag = entry.address & mask

		mask = 0
		for i in range(1 , cache.index + 1):
			mask |= (1 << (16 - (cache.tag + i)))
		address_index = entry.address & mask
		address_index >>= cache.offset

		r = random.randint(1,cache.set_size)

		for x in cache.entries[address_index].keys():
			if(r == 0):
				temp = cache.entries[address_index][x]
				del cache.entries[address_index][x]
				cache.entries[address_index][address_tag] = entry
				break

			r -= 1

		if(temp.dirty_bit == 1):
			m.replace(temp,cache.child)




a = Cache(512,16,2,4,"wb",None)
m = MemoryHierarchy(a , 20)
m.search(50, a)