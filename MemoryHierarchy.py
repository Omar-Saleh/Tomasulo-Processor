from Entry import *
from Cache import *
from Parser import *
import random

class MemoryHierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, filename, main_memory_access_time):
		self.elapsed_time = 0
		#self.main_memory = {50: "aa" , test: "ab"}
		self.main_memory_access_time = main_memory_access_time
		self.registerValues = {}
		for i in range(31):
			self.registerValues['r' + str(i)] = 0
		self.parser = Parser(filename)
		self.level1_cache = None
		self.create()
		self.pc = self.parser.pc
		self.instructions = self.parser.instructions
		#for i in range(len(self.instructions)):
	 	#	self.search(self.pc, self.level1_cache)
	 	#	self.pc += 2
	 	#	print("First Instruction Over")


	def search(self, address, cache):
	# 	Binary Conversion 
	#	tag = address[:tag_bits]
	#	index = address[tag_bits:tag_bits+index_bits]
	#	offset = address[-offset_bits:]
	#	print(cache.child)
		""" Using Numbers instead of binary the mask only sets
		the tag bits for the address_tag and the index bits for the index_tag """
		address_tag = calculate_tag(address, cache.tag, cache.index, cache.offset)
		address_index = calculate_index(address, cache.tag, cache.index, cache.offset)
		# Checking with the address_index and address_tag for the entry
		# print(address_index)
		# print(mask)
		# print(cache)
		if address_tag in cache.entries[address_index]:
			cache.hits += 1
			self.elapsed_time += cache.cycle_time
			if cache.parent != None:
				self.update(cache.entries[address_index][address_tag] , cache.parent)
		# Address Not Found Need to look in the next child
		else:
			cache.misses += 1
			if cache.child != None:
				self.elapsed_time += cache.cycle_time
				self.search(address, cache.child)
			else:
			# Fetching From Main Memory...Need to create a new entry and propagate it upwards to all cache levels
				# print("here")
				self.elapsed_time += cache.cycle_time + self.main_memory_access_time
				e = Entry(1, 0, address)
				self.update(e, cache) #+ main memory cycle time 
			
	#def search(address , cache):
		
# Update should update all the cache blocks above the level where the entry was found
	def update(self, entry, cache):
		# print("Checkpoint")
		# print(entry , cache)
		address_tag = calculate_tag(entry.address, cache.tag, cache.index, cache.offset)
		address_index = calculate_index(entry.address, cache.tag, cache.index, cache.offset)

		if len(cache.entries[address_index]) == cache.set_size:
			self.replace(entry, cache)
		else:
			cache.entries[address_index][address_tag] = entry

		if cache.parent != None:
			self.elapsed_time += cache.cycle_time
			self.update(entry,cache.parent)
		# else:
			# print("Last")


# Write Back should write down to a cache/main memory if there was no empty space to write and the entry was marked as dirty
	def replace(self, entry, cache):
		#pass
		address_tag = calculate_tag(entry.address, cache.tag, cache.index, cache.offset)
		address_index = calculate_index(entry.address, cache.tag, cache.index, cache.offset)

		r = random.randint(0,cache.set_size - 1)
		resolved = False
		for tag in cache.entries[address_index].keys():
			if cache.entries[address_index][tag].valid_bit == 0:
				del cache.entries[address_index][tag]
				resolved = True
				break
		temp = entry
		if not resolved:
			for tag in cache.entries[address_index].keys():
				if r == 0:
					temp = cache.entries[address_index][tag]
					del cache.entries[address_index][tag]
					break
				r -= 1
		cache.entries[address_index][address_tag] = entry			
		if temp.dirty_bit == 1:
			# Still Propagating in cache
			if cache.child != None:
				self.replace(temp,cache.child)
			# Reached Main Memory
			else:
				pass

	def create(self):
		array = self.parser.cacheArray
		parent = None
		for i in range(len(array)):
			c  = Cache(int(array[i][0]),int(array[i][1]),int(array[i][2]),int(array[i][3]),array[i][1],parent)
			if i == 0 :
				self.level1_cache = c

			parent = c


def calculate_tag(address, tag_bits, index_bits, offset_bits):
	mask = 0
	for i in range(1 , tag_bits + 1):
		mask |= (1 << (16 - i))
	address_tag = address & mask
	# print(bin(mask))
	address_tag >>= (offset_bits + index_bits)
	return address_tag

def calculate_index(address, tag_bits, index_bits, offset_bits):
	mask = 0
	for i in range(1 , index_bits + 1):
		mask |= (1 << (16 - (tag_bits + i)))
	address_index = address & mask
	address_index >>= offset_bits
	return address_index

# a = Cache(512,16,1,4,"wb",None)
# m = MemoryHierarchy(a , 20)
# m.search(50, a)
# print(m.i_cache.entries[3])
# m.search(int("111000110001" , 2) , a)
# # print(m.i_cache)
# # print(m.i_cache.entries[3])
# # print(int("111000110001" , 2))
# print(m.i_cache.entries[3])
# #print(tag(int("1100000000000000" , 2) , 6, 5 ,5))
#Testing 
#m = MemoryHierarchy("file.txt",20)
#print(m.level1_cache.misses , m.level1_cache.hits)