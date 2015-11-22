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
	# 	Binary Conversion 
	#	tag = address[:tag_bits]
	#	index = address[tag_bits:tag_bits+index_bits]
	#	offset = address[-offset_bits:]

		""" Using Numbers instead of binary the mask only sets
		the tag bits for the address_tag and the index bits for the index_tag """
		address_tag = tag(address, cache.tag, cache.index, cache.offset)
		address_index = index(address, cache.tag, cache.index, cache.offset)
		# Checking with the address_index and address_tag for the entry
		# print(address_index)
		# print(mask)
		# print(cache)
		if address_tag in cache.entries[address_index]:
			self.elapsed_time += cache.hit_cycle_time
			self.update(entries[address_index][address_tag] , cache.parent)
		if cache.child != None:
			self.elapsed_time += cache.cycle_time
			search(address, cache.chid)
		else:
		# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
			self.elapsed_time += cache.cycle_time + self.main_memory_access_time
			e = Entry(1, 0, 50, "aa")
			self.update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		
# Update should update all the cache blocks above the level where the entry was found
	def update(self, entry, cache):
		#pass
		address_tag = tag(entry.address, cache.tag, cache.index, cache.offset)
		address_index = index(entry.address, cache.tag, cache.index, cache.offset)

		if len(cache.entries[address_index]) == cache.set_size:
			self.replace(entry, cache)
		else:
			cache.entries[address_index][address_tag] = entry

		if cache.parent != None:
			self.elapsed_time += cache.cycle_time
			self.update(entry,cache.parent)


# Write Back should write down to a cache/main memory if there was no empty space to write and the entry was marked as dirty
	def replace(self, entry, cache):
		#pass
		address_tag = tag(entry.address, cache.tag, cache.index, cache.offset)
		address_index = index(entry.address, cache.tag, cache.index, cache.offset)

		r = random.randint(0,cache.set_size - 1)
		temp = entry
		for x in cache.entries[address_index].keys():
			if r == 0:
				temp = cache.entries[address_index][x]
				del cache.entries[address_index][x]
				cache.entries[address_index][address_tag] = entry
				break
			r -= 1

		if temp.dirty_bit == 1:
			# Still Propagating in cache
			if cache.child != None:
				self.replace(temp,cache.child)
			# Reached Main Memory
			else:
				pass


def tag(address, tag_bits, index_bits, offset_bits):
	mask = 0
	for i in range(1 , tag_bits + 1):
		mask |= (1 << (16 - i))
	address_tag = address & mask
	print(bin(mask))
	address_tag >>= (offset_bits + index_bits)
	return address_tag

def index(address, tag_bits, index_bits, offset_bits):
	mask = 0
	for i in range(1 , index_bits + 1):
		mask |= (1 << (16 - (tag_bits + i)))
	address_index = address & mask
	address_index >>= offset_bits
	return address_index

a = Cache(512,16,1,4,"wb",None)
m = MemoryHierarchy(a , 20)
# m.search(50, a)
# print(m.i_cache)
# print(m.i_cache.entries[3])
# print(int("111000110001" , 2))
# m.replace(Entry(1 , 1 ,int("111000110001" , 2), "ab"), m.i_cache)
# print(m.i_cache.entries[3])
#print(tag(int("1100000000000000" , 2) , 6, 5 ,5))