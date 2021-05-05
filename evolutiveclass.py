from constants import FORWARD, RIGHT, LEFT
from robotclass import Sensor
'''
# TODO evolutive algorithm
RANDOM_SEED = 20200504
POP_SIZE = 30
CROSSOVER_RATE = 70
MUTATION_RATE = 3
'''
class Evolutive:
	def __init__(self, nSensors):
		self.nSensors = nSensors

	def sensorInit(self):
		fSensor = Sensor((30, 0), FORWARD, (0, 0, 255))
		lSensor = Sensor((15, -20), LEFT, (0, 0, 255))
		rSensor = Sensor((15, 20), RIGHT, (0, 0, 255))

		lineSensors = (fSensor, lSensor, rSensor)
		return lineSensors
		