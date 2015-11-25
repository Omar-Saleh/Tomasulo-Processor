class Parser(object):
	"""docstring fos Parser"""
	def __init__(self, filename):
		#supes Parser, self).__init__()
		#elf.arg = arg
		number = int(input("Please enter the number of caches: "))
		with open(filename , "r+") as my_file:
			lines = my_file.read().splitlines()
		self.cache_array = []
		i = 0
		while i in range(number): 
			self.cache_array.append(lines[i].replace('(' , ' ').split()[1].replace(')',' ').split()[0].replace(',',' ').split())
			i += 1
		while ".org" not in lines[i].lower():
			i += 1

		# Support For Hexadecimal or decimal starting address
		# Starting address is saved in self.pc
		starting_address = lines[i].split(' ')[1]
		if len(starting_address) > 2 and starting_address[0] == '0' and starting_address[1] == 'x':
			self.pc = int(starting_address , 16)
		else:
			self.pc = int(starting_address)
		i += 1

		# Reading Instructions and indexing labels
		# Labels are indexed in self.labels
		instructions = [lines[i].replace(',' , ' ').split()]
		print(self.pc)

p = Parser("file.txt")