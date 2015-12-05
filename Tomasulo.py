from MemoryHierarchy import *
from ReservationStation import *
from InstructionBuffer import *
from ROB import *
from RegisterStatus import *

class Tomasulo(object):
	"""docstring for Tomasulo"""
	def __init__(self , filename):
		self.reservationStations = [] 
		main_memoy_cycle_time = int(input("Please the number of cycles required to access the memory: "))
		self.m = MemoryHierarchy(filename,main_memoy_cycle_time)
		self.registerFile = self.m.registerValues
		self.memory = self.m.main_memory
		#print(m.instructions)
		self.instructions = self.m.instructions
		self.registerStatus = RegisterStatus()
		ROBSize = int(input("Please enter ROB size: "))
		self.rob = ROB(ROBSize)
		self.pipelineWidth = int(input("Please enter pipeline width: "))
		bufferSize = int(input("Please enter size of instruction buffer: "))	
		AddUnitSize = int(input("Please enter number of ADD Units: "))
		AddUnitCycle = int(input("Please enter number of ADD Units cycles: "))
		MULTUnitSize = int(input("Please enter number of MULT Units: "))
		MULTUnitCycles = int(input("Please enter number of MULT Units cycles: "))
		LDSTUnitSize = int(input("Please enter number of LD/ST Units: "))
		LDSTUnitCycle = int(input("Please enter number of LD/ST Units cycles: "))
		LogicUnitSize = int(input("Please enter number of Logic Units: "))
		LogicUnitCycle = int(input("Please enter number of Logic Unit cycles: "))

		for i in range(AddUnitSize):
			self.reservationStations.append(ReservationStation("ADD",AddUnitCycle))

		for i in range(MULTUnitSize):
			self.reservationStations.append(ReservationStation("MUL",MULTUnitCycles))

		for i in range(LDSTUnitSize):
			self.reservationStations.append(ReservationStation("LDST",LDSTUnitCycle))

		for i in range(LogicUnitSize):
			self.reservationStations.append(ReservationStation("LOGIC", LogicUnitCycle))


		self.currentPC = self.m.pc
		self.instructionBuffer = InstructionBuffer(bufferSize)
		self.branchOverride = None
		self.toggleBranch = False
		self.totalBranches = 0
		self.branchMissPredictions = 0
		self.registerFile['r1'] = 20
		self.tempRegisterFile = self.registerFile
		cycles = 0
		# print(self.instructions)
		while self.currentPC in self.instructions.keys() or self.rob.ROB_Entries[self.rob.head % self.rob.size] != None or self.instructionBuffer.peek() != None:
		# for i in range(10):
			cycles += 1
			self.commit()
			self.writeBack()
			self.execute()
			self.issue()
			self.fetch()
			print(self.instructionBuffer.buffer)
			print(self.registerFile)
			print(self.rob.ROB_Entries)
			print("-----")

		print(cycles)
			
	def fetch(self):
		for i in range(self.pipelineWidth):
			print(self.currentPC)
			if self.branchOverride != None:
				# print("here")
				self.currentPC = int(self.branchOverride)
				self.branchOverride = None
			if not self.instructionBuffer.isFull() and self.currentPC in self.instructions.keys():
				if self.instructions[self.currentPC][0].lower() in self.m.parser.branchingInstructions:
					if self.instructions[self.currentPC][0].lower() == "jmp" and self.registerStatus.registers[self.instructions[self.currentPC][1]] == None:
						self.instructionBuffer.insert(self.instructions[self.currentPC])
						self.currentPC += 2 + self.tempRegisterFile[self.instructions[self.currentPC][1]] + int(self.instructions[self.currentPC][2])
					elif self.instructions[self.currentPC][0].lower() == "beq":
						if int(self.instructions[self.currentPC][3]) < 0:
							self.instructions[self.currentPC].append(self.currentPC + 2)
							self.instructionBuffer.insert(self.instructions[self.currentPC])
							self.currentPC += 2 + int(self.instructions[self.currentPC][3])
						else:
							# print(self.instructions[self.currentPC])
							self.instructions[self.currentPC].append(self.currentPC + 2)
							self.instructionBuffer.insert(self.instructions[self.currentPC])
							self.currentPC += 2
					elif self.instructions[self.currentPC][0].lower() == 'jalr' and self.registerStatus.registers[self.instructions[self.currentPC][2]] == None:
						temp = self.instructions[self.currentPC][2]
						self.instructions[self.currentPC][2] = (self.currentPC + 2)
						self.instructionBuffer.insert(self.instructions[self.currentPC])
						self.registerStatus.registers[self.instructions[self.currentPC][1]] = "BLOCK"
						self.currentPC = self.tempRegisterFile[temp]
					elif self.instructions[self.currentPC][0].lower() == 'ret' and self.registerStatus.registers[self.instructions[self.currentPC][1]] == None:
						self.instructionBuffer.insert(self.instructions[self.currentPC])
						self.currentPC = self.tempRegisterFile[self.instructions[self.currentPC][1]]
						print(self.currentPC)
					else:
						break
				else:
					self.instructionBuffer.insert(self.instructions[self.currentPC])
					self.currentPC += 2

	def issue(self):
		#checking rob
		count = 0
		while self.instructionBuffer.peek() != None and not self.rob.isFull():
			# print("HI")
			instruction = self.instructionBuffer.peek()
			if instruction[0] in self.m.parser.addInstructions or instruction[0] in self.m.parser.branchingInstructions:    #check if its in the add unit
				if not self.helper(instruction, "ADD"):
					break
			elif instruction[0] in self.m.parser.mulInstructions :
				if not self.helper(instruction, "MUL"):
					break
			elif instruction[0] in self.m.parser.ldstInstructions :
				if not self.helper(instruction, "LDST"):
					break
			elif instruction[0] == "nand":
				if not self.helper(instruction , "LOGIC") :
					break
			else:
				self.instructionBuffer.issue()
			count += 1

		# print("COUNT IS THE COUNT COUNT COUNT" , count)

	def helper(self,instruction, s):
		# print("here")
		# print(instruction)
		reservedPlace = False
		for i in range(len(self.reservationStations)):
			# print(self.reservationStations[i].busy)
			#print(not self.reservationStations[i].check(), self.reservationStations[i].name, s)
			if self.reservationStations[i].name == s and not self.reservationStations[i].check():
				# print("here")
				# print(instruction)
				reservedPlace = True
				address = None
				branchOffset = None
				self.instructionBuffer.issue()
				entryNumber = self.rob.add(instruction[0],instruction[1],None)

				if s == "MUL" or s == "ADD" or s == "LDST" or s == "LOGIC":
					if instruction[0] == 'beq':
						# print(instruction)
						if self.registerStatus.registers[instruction[2]] == None:
							readySource2 = instruction[2]
							notReadySource2 = None
						else:
							readySource2 = None
							notReadySource2 = instruction[2]
						if self.registerStatus.registers[instruction[1]] == None :
							readySource1 = instruction[1]
							notReadySource1 = None
						else :
							readySource1 = None
							notReadySource1 = instruction[1]
						address = instruction[4]
						branchOffset = instruction[3]
						# print(address, branchOffset, "First")
					elif instruction[0] == 'jalr':
						notReadySource2 = None
						notReadySource1 = None
						readySource1 = instruction[2]
						readySource2 = None
					elif instruction[0] == 'jmp' or instruction[0] == 'ret':
						notReadySource1 = None
						notReadySource2 = None
						readySource1 = None
						readySource2 = None
					else:
						if self.registerStatus.registers[instruction[2]] == None :
							readySource1 = instruction[2]
							notReadySource1 = None
						else :
							readySource1 = None
							notReadySource1 = instruction[2]

						if 'r' in instruction[3] and self.registerStatus.registers[instruction[3]] == None:
							readySource2 = instruction[3]
							notReadySource2 = None
						elif 'r' in instruction[3] and self.registerStatus.registers[instruction[3]] != None:
							readySource2 = None
							notReadySource2 = instruction[3]
						else:
							readySource2 = instruction[3]
							notReadySource2 = None
				self.registerStatus.registers[instruction[1]] = entryNumber
				# print(address, branchOffset, "SECOND")
				self.reservationStations[i].reserve(instruction[0], readySource1 , readySource2 , notReadySource1 , notReadySource2 , entryNumber , address, branchOffset)
				# print(self.reservationStations[i].address, self.reservationStations[i].branchOffset)
				break
		if reservedPlace:
			return True
		else:
			return False

	def execute(self):
		for i in range(len(self.reservationStations)):
			currentStation = self.reservationStations[i]
			if currentStation.check():
				if currentStation.notReadySource1 != None :
					# print("!!!!!!!!!!!!!!!" , currentStation.notReadySource1)
					if self.registerStatus.registers[currentStation.notReadySource1] == None:
						currentStation.readySource1 = currentStation.notReadySource1
						currentStation.notReadySource1 = None

				if currentStation.notReadySource2  != None :
					if self.registerStatus.registers[currentStation.notReadySource2] == None :
						currentStation.readySource2 = currentStation.notReadySource2
						currentStation.notReadySource2 = None

				if currentStation.notReadySource1 == None and currentStation.notReadySource2 == None:
					currentStation.execute() # it decrements current cycles 
						

	def writeBack(self):
		for i in range(len(self.reservationStations)):
			currentStation = self.reservationStations[i]
			# print("kkkkk")
			# print(currentStation.currentCycles )
			if currentStation.busy and currentStation.currentCycles == 0:
				result = self.calculate(currentStation.op , currentStation.readySource1, currentStation.readySource2, currentStation.address, currentStation.branchOffset)
				# print(result, "!!@#!@#!$")
				if self.rob.ROB_Entries[currentStation.dest % self.rob.size] != None:
					self.rob.update(result,currentStation.dest)
					registerName = self.rob.ROB_Entries[currentStation.dest % self.rob.size].dest
					# print(registerName)
					# print("-----")
					#self.registerFile[registerName] = result
					if self.rob.ROB_Entries[self.rob.head % self.rob.size].type != 'beq' and self.rob.ROB_Entries[currentStation.dest % self.rob.size].type != 'jmp' and self.rob.ROB_Entries[currentStation.dest % self.rob.size].type != 'sw' and self.rob.ROB_Entries[currentStation.dest % self.rob.size].type != 'ret':
						self.tempRegisterFile[registerName] = result
					self.registerStatus.registers[registerName] = None
					currentStation.currentCycles = currentStation.cycles
					currentStation.busy = False

	def commit(self):
		# print(self.rob.ROB_Entries[self.rob.head % self.rob.size])
		if self.rob.ROB_Entries[self.rob.head % self.rob.size] != None and self.rob.ROB_Entries[self.rob.head % self.rob.size].ready:
			if self.rob.ROB_Entries[self.rob.head % self.rob.size].type == 'beq':
				if self.toggleBranch == True:
					# print("here")
					self.toggleBranch = False
					self.branchOverride = self.rob.ROB_Entries[self.rob.head % self.rob.size].value
					self.rob.flush()
					self.instructionBuffer.flush()
					self.tempRegisterFile = self.registerFile
					for i in range(len(self.reservationStations)):
						self.reservationStations[i].flush()
				else:
					self.rob.commit()
			elif self.rob.ROB_Entries[self.rob.head % self.rob.size].type == 'jmp' or self.rob.ROB_Entries[self.rob.head % self.rob.size].type == 'sw' or self.rob.ROB_Entries[self.rob.head % self.rob.size].type == 'ret':
				self.rob.commit()
			else:
				registerName = self.rob.ROB_Entries[self.rob.head % self.rob.size].dest
				# print(registerName,  self.rob.ROB_Entries[self.rob.head % self.rob.size].value, "!!!!!!!!!!!!!!!!!!!!")
				self.registerFile[registerName] = self.rob.ROB_Entries[self.rob.head % self.rob.size].value
				self.rob.commit()


	def calculate(self,op, source1 , source2, address, branchOffset):
		if op == "addi":
			print(source1, self.tempRegisterFile)
			a= self.tempRegisterFile[source1]
			return a + int(source2)  # not a source its just a number
		elif op == "add":
			a = self.tempRegisterFile[source1]
			b = self.tempRegisterFile[source2]
			return a + b
		elif op == "sub" :
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			return a - b
		elif op == "mul":
			a = self.tempRegisterFile[source1]
			b = self.tempRegisterFile[source2]
			return a * b	
		elif op == "div":
			a = self.tempRegisterFile[source1]
			b = self.tempRegisterFile[source2]
			# print(source1, source2, self.registerFile[source1], self.registerFile[source2])
			return a // b
		elif op == "lw":
			address = self.tempRegisterFile[source1] + int(source2)
			self.m.search(self.m.d_cache, address)
			result = self.memory[int(address)]
			return result
		elif op == "sw":
			address = self.tempRegisterFile[source1] + int(source2)
			self.m.search(self.m.d_cache,address)
			if self.m.d_cache.writing_policy == "wt":
				entry = Entry(1,0,address)
				self.m.replace(entry,self.m.d_cache,False)
			else :
				entry = Entry(1,1,address)
				self.m.replace(entry,self.m.d_cache,True)

		elif op == "nand":
			a = self.tempRegisterFile[source1]
			b = self.tempRegisterFile[source2]
			return (~(a & b))
		elif op == 'beq':
			self.totalBranches += 1
			a = self.tempRegisterFile[source1]
			b = self.tempRegisterFile[source2]
			# print(a , b , branchOffset, address)
			if a == b and int(branchOffset) > 0:
				self.branchMissPredictions += 1
				self.toggleBranch = True
				return int(address) + int(branchOffset)
			elif a != b and int(branchOffset) < 0:
				self.branchMissPredictions += 1
				self.toggleBranch = True
				return int(address)
			else:
				return None
		elif op == 'jalr':
			a = int(source1)
			return a
		else:   
			return None		

# def offset_conversion(number):
# 	pass
filename = input("Please enter the file name required to run: ")
t = Tomasulo(filename)
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# t.commit()
# t.writeBack()
# t.execute()
# t.issue()
# t.fetch()
# print(t.instructionBuffer.buffer)
# print(t.registerFile)
# print(t.rob.ROB_Entries)
# print("-----")
# # print(t.rob.head)
# # print(t.rob.tail)
# # print(t.registerStatus.registers)
# # print(t.instructionBuffer.buffer)

# temp = t.m.d_cache
# for i in range(4):

# 	print(temp.entries)
# 	print("_________")
# 	temp = temp.child

