class Parser(object):
	"""docstring fos Parser"""
	def __init__(self, filename):
		#supes Parser, self).__init__()
		#elf.arg = arg
		number = int(input("Please enter the number of caches: "))
		with open(filename , "r+") as my_file:
			lines = my_file.read().splitlines()
		self.cache_array = []
		for i in range(number): 
			self.cache_array.append(lines[i].replace('(' , ' ').split()[1].replace(')',' ').split()[0].replace(',',' ').split())


			



