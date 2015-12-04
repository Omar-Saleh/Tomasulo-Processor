from Entry import *
from Cache import *
from Parser import *
import random

class MemoryHierarchy(object):
	"""docstring for Memory-hierarchy  : cache_l1 is the level 1 cache  , line is the  16 bit address"""
	def __init__(self, filename, main_memory_access_time):
		self.elapsed_time = 0
		self.main_memory = {50: 1250}
		self.main_memory_access_time = main_memory_access_time
		self.registerValues = {}
		for i in range(31):
			self.registerValues['r' + str(i)] = 5
		self.parser = Parser(filename)
		self.level1_cache = None
		self.create()
		self.pc = self.parser.pc
		self.instructions = self.parser.instructions
		#for i in range(len(self.instructions)):
	 	#	self.search(self.pc, self.level1_cache)
	 	#	self.pc += 2
	 	#	print("First Instruction Over")


	def search(self, cache, address):
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
				self.search(cache.child, address)
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
			self.replace(entry, cache,True)
		else:
			cache.entries[address_index][address_tag] = entry

		if cache.parent != None:
			self.elapsed_time += cache.cycle_time
			self.update(entry,cache.parent)
		# else:
			# print("Last")




# Write Back should write down to a cache/main memory if there was no empty space to write and the entry was marked as dirty
# if flag = true then its write back if its = false then its write through
	def replace(self, entry, cache , flag):
		#pass
		address_tag = calculate_tag(entry.address, cache.tag, cache.index, cache.offset)
		address_index = calculate_index(entry.address, cache.tag, cache.index, cache.offset)
		if len(cache.entries[address_index]) == cache.set_size or address_tag in cache.entries[address_index].keys():
			

			r = random.randint(0,cache.set_size - 1)
			resolved = False
			for tag in cache.entries[address_index].keys():
				if cache.entries[address_index][tag].valid_bit == 0:
					del cache.entries[address_index][tag]
					resolved = True
					break

			if not resolved :
				for tag in cache.entries[address_index].keys():
					if cache.entries[address_index][tag].dirty_bit == 0:
						del cache.entries[address_index][tag]
						resolved = True
						break

			temp = None

			if not resolved:
				for tag in cache.entries[address_index].keys():
					if r == 0:
						temp = cache.entries[address_index][tag]
						del cache.entries[address_index][tag]
						break
					r -= 1
			cache.entries[address_index][address_tag] = entry

			if not resolved and temp.dirty_bit == 1:
				# Still Propagating in cache

				if cache.child != None:
					if cache.child.writing_policy == "wt" :
						self.replace(temp,cache.child,False) 
					else :
						self.replace(temp,cache.child,True)

				# Reached Main Memory
				else:
					pass

			if flag == False and cache.child != None :
				self.replace(entry,cache.child,False)
		else :
			cache.entries[address_index][address_tag] = entry

			if cache.child != None and flag == False:
				self.elapsed_time += cache.cycle_time
				self.replace(entry,cache.child,False)



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

a = Cache(512,16,1,4,"wb",None)
m = MemoryHierarchy("file.txt" , 20)

m.search(m.level1_cache,128)
m.search(m.level1_cache,256)
m.search(m.level1_cache,512)
m.search(m.level1_cache,1024)
m.search(m.level1_cache,2048)

e = Entry(1,1,50)
m.replace(e, m.level1_cache,False)
temp = m.level1_cache
for i in range(4):

	print(temp.entries)
	print("_________")
	temp = temp.child

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
