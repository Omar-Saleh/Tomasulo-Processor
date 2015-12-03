from MemoryHierarchy import *
from ReservationStation import *
from InstructionBuffer import *
from ROB import *
from RegisterStatus import *

class Tomasulo(object):
	"""docstring for Tomasulo"""
	def __init__(self , filename):
		self.reservationStations = [] 
		self.m = MemoryHierarchy(filename,20)
		self.registerFile = self.m.registerValues
		self.memory = self.m.main_memory
		#print(m.instructions)
		self.instructions = self.m.instructions
		self.registerStatus = RegisterStatus()
		ROBSize = int(input("Please enter ROB size: "))
		self.rob = ROB(self.ROBSize)
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
			self.reservationStations.append(ReservationStation("Logic", LogicUnitCycle))

		self.currentPC = self.m.pc
		self.instructionBuffer = InstructionBuffer(self.bufferSize)

	def fetch(self):
		for i in range(self.pipelineWidth):
			if not self.instructionBuffer.isFull() and self.currentPC in self.instructions.keys():
				self.instructionBuffer.insert(self.instructions[self.currentPC])
				if self.instructions[self.currentPC][0].lower() in self.m.parser.branchingInstructions:
					if self.instructions[self.currentPC][0] == "jmp" and self.registerStatus.registers[self.instructions[self.currentPC][1]] == None:
						self.instructionBuffer.insert(self.instructions[self.currentPC])
						self.currentPC += 2 + self.registerFile[self.instructions[self.currentPC][1]] + int(self.instructions[self.currentPC][2])
					elif self.instructions[self.currentPC][0] == "beq":
						if self.instructions[self.currentPC][3] & (1 << 6) != 0:
							pass
						else:
							pass
				else:
					self.currentPC += 2

	def issue(self):
		#checking rob
		count = 0
		while self.instructionBuffer.peek() != None and not self.rob.isFull():
			# print("HI")
			instruction = self.instructionBuffer.peek()
			if instruction[0] in self.m.parser.addInstructions :    #check if its in the add unit
				if not self.helper(instruction, "ADD"):
					break
			elif instruction[0] in self.m.parser.mulInstructions :
				if not self.helper(instruction, "MUL"):
					break
			elif instruction[0] in self.m.parser.ldstInstructions :
				if not self.helper(instruction, "LDST"):
					break
			else:
				self.instructionBuffer.issue()
			count += 1

		# print("COUNT IS THE COUNT COUNT COUNT" , count)

	def helper(self,instruction, s):
		# print("here")
		reservedPlace = False
		for i in range(len(self.reservationStations)):
			#print(not self.reservationStations[i].check(), self.reservationStations[i].name, s)
			if self.reservationStations[i].name == s and not self.reservationStations[i].check():
				# print("here")
				# print(instruction)
				reservedPlace = True
				address = None
				self.instructionBuffer.issue()
				entryNumber = self.rob.add(instruction[0],instruction[1],None)
				if s == "MUL" or s == "ADD" or s == "LDST" or s == "Logic":
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
				else:
					pass
				self.registerStatus.registers[instruction[1]] = entryNumber
				self.reservationStations[i].reserve(instruction[0], readySource1 , readySource2 , notReadySource1 , notReadySource2 , entryNumber , address)
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
				result = self.calculate(currentStation.op , currentStation.readySource1, currentStation.readySource2)
				# print(result, "!!@#!@#!$")
				if self.rob.ROB_Entries[currentStation.dest % self.rob.size] != None
					self.rob.update(result,currentStation.dest)
					registerName = self.rob.ROB_Entries[currentStation.dest % self.rob.size].dest
					# print(registerName)
					# print("-----")
					#self.registerFile[registerName] = result
					self.registerStatus.registers[registerName] = None
					currentStation.currentCycles = currentStation.cycles
					currentStation.busy = False

	def commit(self):
		# print(self.rob.ROB_Entries[self.rob.head % self.rob.size])
		if self.rob.ROB_Entries[self.rob.head % self.rob.size] != None and self.rob.ROB_Entries[self.rob.head % self.rob.size].ready:
			registerName = self.rob.ROB_Entries[self.rob.head % self.rob.size].dest
			# print(registerName,  self.rob.ROB_Entries[self.rob.head % self.rob.size].value, "!!!!!!!!!!!!!!!!!!!!")
			self.registerFile[registerName] = self.rob.ROB_Entries[self.rob.head % self.rob.size].value
			self.rob.commit()


	def calculate(self,op, source1 , source2):
		if op == "addi":
			a= self.registerFile[source1]
			return a + int(source2)  # not a source its just a number
		elif op == "add":
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			return a + b
		elif op == "sub" :
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			return a - b
		elif op == "mul":
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			return a * b	
		elif op == "div":
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			# print(source1, source2, self.registerFile[source1], self.registerFile[source2])
			return a // b
		elif op == "lw":
			address = self.registerFile[source1] + int(source2)
			self.m.search(self.m.level1_cache, address)
			result = self.memory[int(address)]
			return result
		elif op == "sw":
			address = self.registerFile[source1] + int(source2)
		elif op == "nand":
			a = self.registerFile[source1]
			b = self.registerFile[source2]
			return (~(a & b))
			 



t = Tomasulo("file.txt")
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
# print(t.rob.head)
# print(t.rob.tail)
# print(t.registerStatus.registers)
# print(t.instructionBuffer.buffer)