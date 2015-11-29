from MemoryHierarchy import *
from ReservationStation import *
class Tomasulo(object):
	"""docstring for Tomasulo"""
	def __init__(self):
		self.reservationStations = [] 
		m = MemoryHierarchy("file.txt",20)
		print(m.instructions)

		self.pipelineWidth = int(input("Please enter pipeline width :"))
		self.bufferSize = int(input("Please enter size of instruction buffer :"))	

		self.AddUnitSize = int(input("Please enter number of ADD units : "))
		self.AddUnitCycle = int(input("Please enter number of ADD units cycles : "))
		self.MULTUnitSize = int(input("Please enter number of MULT units : "))
		self.MULTUnitCycles = int(input("Please enter number of MULT units cycles : "))
		self.LDSTUnitSize = int(input("Please enter number of LD/ST units : "))
		self.LDSTUnitCycle = int(input("Please enter number of LD/ST units cycles : "))

		for i in range(self.AddUnitSize):
			self.reservationStations.append(ReservationStation("Add",self.AddUnitCycle))

		for i in range(self.MULTUnitSize):
			self.reservationStations.append(ReservationStation("MULT",self.MULTUnitCycles))

		for i in range(self.LDSTUnitSize):
			self.reservationStations.append(ReservationStation("LDST",self.LDSTUnitCycle))


		self.instructionBuffer = [None] * self.bufferSize
		


		





t = Tomasulo()