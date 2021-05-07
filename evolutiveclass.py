from constants import FORWARD, RIGHT, LEFT
from robotclass import Robot, LineSensor
from random import randint, seed

# TODO evolutive algorithm
RANDOM_SEED = 20200504
POP_SIZE = 30
CROSSOVER_RATE = 70
MUTATION_RATE = 3

class Evolutive:
	def __init__(self):
		seed(RANDOM_SEED)

		self.population = self.popInit()
	
	def popInit(self):
		population = []
		
		for p in range(POP_SIZE):
			parent = []
			
			# Create random positions for the robot's line sensors
			fSensor = LineSensor((0, 0, 255), 3, FORWARD, (randint(0,0), randint(0,0))) # Forward sensor
			lSensor = LineSensor((0, 0, 255), 3, LEFT, (randint(-50,50), randint(-50,50))) # Left sensor
			rSensor = LineSensor((0, 0, 255), 3, RIGHT, (randint(-50,50), randint(-50,50))) # Right sensor
			
			'''
			fSensor = LineSensor((0, 0, 255), 3, FORWARD, (30,0)) # Forward sensor
			lSensor = LineSensor((0, 0, 255), 3, LEFT, (30,-50)) # Left sensor
			rSensor = LineSensor((0, 0, 255), 3, RIGHT, (30,50)) # Right sensor
			'''
			parent = (fSensor, lSensor, rSensor)
			population.append(parent)

		return population

	def robotInit(self, track, curRobotIndex):
		curLineSensors = self.population[curRobotIndex]
		curRobot = Robot(track.vertices[0], curLineSensors, track.vertices)

		return curRobot

