from MemoryHierarchy import *
from ReservationStation import *
from InstructionBuffer import *
from ROB import *
from RegisterStatus import *

class Tomasulo(object):
	"""docstring for Tomasulo"""
	def __init__(self):
		self.reservationStations = [] 
		self.m = MemoryHierarchy("file.txt",20)
		self.registerFile = self.m.registerValues
		self.memory = self.m.main_memory
		#print(m.instructions)
		self.instructions = self.m.instructions
		self.registerStatus = RegisterStatus()
		self.ROBSize = int(input("Please enter ROB size : "))
		self.rob = ROB(self.ROBSize)
		self.pipelineWidth = int(input("Please enter pipeline width :"))
		self.bufferSize = int(input("Please enter size of instruction buffer :"))	
		self.AddUnitSize = int(input("Please enter number of ADD units : "))
		self.AddUnitCycle = int(input("Please enter number of ADD units cycles : "))
		self.MULTUnitSize = int(input("Please enter number of MULT units : "))
		self.MULTUnitCycles = int(input("Please enter number of MULT units cycles : "))
		self.LDSTUnitSize = int(input("Please enter number of LD/ST units : "))
		self.LDSTUnitCycle = int(input("Please enter number of LD/ST units cycles : "))

		for i in range(self.AddUnitSize):
			self.reservationStations.append(ReservationStation("ADD",self.AddUnitCycle))

		for i in range(self.MULTUnitSize):
			self.reservationStations.append(ReservationStation("MUL",self.MULTUnitCycles))

		for i in range(self.LDSTUnitSize):
			self.reservationStations.append(ReservationStation("LDST",self.LDSTUnitCycle))

		self.currentPC = self.m.pc
		self.instructionBuffer = InstructionBuffer(self.bufferSize)

	def fetch(self):
		for i in range(self.pipelineWidth):
			if not self.instructionBuffer.isFull() and self.currentPC in self.instructions.keys():
				self.instructionBuffer.insert(self.instructions[self.currentPC])
				if self.instructions[self.currentPC][0].lower() in self.m.parser.branchingInstructions :
					pass	
				else :
					self.currentPC += 2

	def issue(self):
		#checking rob
		if not self.rob.isFull():
			print("HI")

			instruction = self.instructionBuffer.peek()
			if instruction[0] in self.m.parser.addInstructions :    #check if its in the add unit
				self.helper(instruction, "ADD")
			elif instruction[0] in self.m.parser.mulInstructions :
				self.helper(instruction, "MUL")
			elif instruction[0] in self.m.parser.ldstInstructions :
				self.helper(instruction, "LDST")

	def helper(self,instruction, s):
		print("here")
		for i in range(len(self.reservationStations)):
			#print(not self.reservationStations[i].check(), self.reservationStations[i].name, s)
			if self.reservationStations[i].name == s and not self.reservationStations[i].check():
				print("here")
				# print(instruction)
				self.instructionBuffer.issue()
				entryNumber = self.rob.add(instruction[0],instruction[1],None)

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
				if s == "LDST":
					pass
				else :
					address = None
				self.reservationStations[i].reserve(instruction[0], readySource1 , readySource2 , notReadySource1 , notReadySource2 , entryNumber , address)
				break

	def execute(self):
		for i in range(len(self.reservationStations)):
			currentStation = self.reservationStations[i]

			if currentStation.check():
				if currentStation.notReadySource1 != None :
					if self.registerStatus.registers[currentStation.notReadySource1] == None :
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
			print("kkkkk")
			print(currentStation.currentCycles )
			if currentStation.busy and currentStation.currentCycles == 0:
				result = self.calculate(currentStation.op , currentStation.readySource1, currentStation.readySource2 ,currentStation.address)
				print(result)
				print("-----")
				self.rob.update(result,currentStation.dest)
				registerName = self.rob.ROB_Entries[currentStation.dest].dest
				#self.registerFile[registerName] = result
				self.registerStatus.registers[registerName] = None
				currentStation.currentCycles = currentStation.cycles
				currentStation.busy = False

	def commit(self):
		print(self.rob.ROB_Entries)
		if self.rob.ROB_Entries[self.rob.head % self.rob.size] != None :
			registerName = self.rob.ROB_Entries[self.rob.head % self.rob.size].dest
			self.registerFile[registerName] = self.rob.ROB_Entries[self.rob.head % self.rob.size].value
			self.rob.commit()


	def calculate(self,op, source1 , source2 , address):
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
			return a // b
		elif op == "lw":
			self.m.search(address)
			result = self.memory[int(address)]
			return result
		elif op == "Sw":
			pass 




					
		

t = Tomasulo()
t.fetch()
print(t.instructionBuffer.buffer)
# print(t.rob.tail)

print(t.instructionBuffer.peek())
t.issue()
# t.issue()
t.execute()
t.writeBack()
t.commit()

print(t.instructionBuffer.peek())
t.issue()
t.execute()
t.writeBack()
t.commit()
print(t.registerFile)
# print(t.rob.head)
# print(t.rob.tail)
# print(t.registerStatus.registers)
# print(t.instructionBuffer.buffer)