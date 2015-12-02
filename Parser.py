class Parser(object):
	"""docstring fos Parser"""
	def __init__(self, filename):
		#supes Parser, self).__init__()
		#elf.arg = arg
		self.branchingInstructions = ["beq","jmp","jalr","ret"]
		self.addInstructions = ["add","sub","addi"]
		self.mulInstructions = ["mul","div"]
		self.ldstInstructions = ["lw","sw"]
		number = int(input("Please enter the number of caches: "))
		with open(filename , "r+") as my_file:
			lines = my_file.read().splitlines()
		self.cacheArray = []
		i = 0
		while i in range(number): 
			self.cacheArray.append(lines[i].replace('(' , ' ').split()[1].replace(')',' ').split()[0].replace(',',' ').split())
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

		self.instructions = [lines[i].replace(',' , ' ') for i in range(i, len(lines))]
		self.labels = {}
		self.scan(self.instructions)
		print(self.instructions)
		for i in range(len(self.instructions)):
			self.instructions[i] = self.format(self.instructions[i])
		indexedInstructions = {}
		tempPc = self.pc
		for i in range(len(self.instructions)):
			indexedInstructions[tempPc] = self.instructions[i]
			tempPc += 2
		self.instructions = indexedInstructions
		print(self.instructions)
		# print(indexedInstructions)
		#print(self.labels)
		# print(self.pc)

	# Index Labels to their respective addresses
	def scan(self, instructions):
		counter = self.pc
		for instruction in instructions:
			if ':' in instruction:
				self.labels[instruction.replace(':', ' ').split()[0]] = counter
			counter += 2

	def format(self, instruction):
		# Removing Labels if there was any
		splitIndex = instruction.find(':')
		if splitIndex > 0:
			instruction = list(instruction)
			instruction[splitIndex - 1] = ' '
			instruction[splitIndex + 1] = ' '
			instruction = "".join(instruction)
		# Splitting the instruction into an array
		instruction = instruction.split()
		if splitIndex > 0:
			instruction = instruction[instruction.index(':') + 1::1]
		return instruction
		#print(instruction)


#p = Parser("file.txt")
