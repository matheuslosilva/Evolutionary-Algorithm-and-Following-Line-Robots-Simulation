from constants import FORWARD, RIGHT, LEFT
from robotclass import Robot, LineSensor
from random import randint, seed

# TODO evolutive algorithm
RANDOM_SEED = 20200504
POP_SIZE = 2
CROSSOVER_RATE = 70
MUTATION_RATE = 3

LEFT_TRACK_LOST_POINTS = -300
LOOP_LOST_POINTS = -500
MISS_COURSE_LOST_POINTS = -200
ITERATIONS_NUMBER_LOST_POINTS = -0.30
COMPLETE_COURSE_EARNED_POINTS = 1000
CHECKPOINTS_NUMBER_EARNED_POINTS = 150
LAPS_NUMBER_EARNED_POINTS = 200


class Evolutive:
    def __init__(self):
        seed(RANDOM_SEED)

        self.population = self.popInit()
        self.fitnessPop = [0 for _ in range(POP_SIZE)] # Stores all the fitness of the population's robots
    
    def popInit(self):
        population = []
        
        for p in range(POP_SIZE):
            parent = []
            '''
            # Create random positions for the robot's line sensors
            fSensor = LineSensor((0, 0, 255), 3, FORWARD, (randint(-50, 50), randint(-50, 50))) # Forward sensor
            lSensor = LineSensor((0, 0, 255), 3, LEFT, (randint(-50, 50), randint(-50, 50))) # Left sensor
            rSensor = LineSensor((0, 0, 255), 3, RIGHT, (randint(-50, 50), randint(-50, 50))) # Right sensor
            '''
            fSensor = LineSensor((0, 0, 255), 3, FORWARD, (40,0)) # Forward sensor
            lSensor = LineSensor((0, 0, 255), 3, LEFT, (35,-20)) # Left sensor
            rSensor = LineSensor((0, 0, 255), 3, RIGHT, (35, 20)) # Right sensor
            
            parent = (fSensor, lSensor, rSensor)
            population.append(parent)

        return population

    def robotInit(self, track, curRobotIndex):
        curLineSensors = self.population[curRobotIndex]
        curRobot = Robot(track.vertices[0], curLineSensors, track.vertices)

        return curRobot

    def evaluateRobotFitness(self, curRobotIndex, curRobotReport):
        fitness = 0
        fitness += curRobotReport["robotLeftTrack"] * LEFT_TRACK_LOST_POINTS
        fitness += curRobotReport["robotInLoop"] * LOOP_LOST_POINTS
        fitness += curRobotReport["robotMissCourse"] * MISS_COURSE_LOST_POINTS
        fitness += curRobotReport["robotIterations"] * ITERATIONS_NUMBER_LOST_POINTS
        fitness += curRobotReport["completeCourse"] * COMPLETE_COURSE_EARNED_POINTS
        fitness += curRobotReport["completeLaps"] * LAPS_NUMBER_EARNED_POINTS
        fitness += curRobotReport["reachedCheckpoints"] * CHECKPOINTS_NUMBER_EARNED_POINTS  

        print(curRobotReport)
        print(fitness) 

        self.fitnessPop[curRobotIndex] += fitness

    def getBestRobotIndex(self):
        maxFitness = 0
        maxFitnessIndex = 0

        for i in range(len(fitnessPop)):
            if fitnessPop[i] > maxFitness:
                maxFitnessIndex = i

        return maxFitnessIndex
'''
TODO
    def crossover(self):


    def mutation(self):


    def tournament2Selection(self):
        indexCompetitor1 = randint(0, (POP_SIZE - 1))
        indexCompetitor2 = randint(0, (POP_SIZE - 1))

        indexCompetitor3 = randint(0, (POP_SIZE - 1))
        indexCompetitor4 = randint(0, (POP_SIZE - 1))
        
        selectedToCrossover = []

        newChromossome
        if self.fitnessPop[indexCompetitor1] >= self.fitnessPop[indexCompetitor2]:
            selectedToCrossover.append(self.population[indexCompetitor1])
        else:
            selectedToCrossover.append(self.population[indexCompetitor2])

        if self.fitnessPop[indexCompetitor3] >= self.fitnessPop[indexCompetitor4]:
            selectedToCrossover.append(self.population[indexCompetitor3])
        else:
            selectedToCrossover.append(self.population[indexCompetitor4])


    def newPopulation(self):
        newPopulation = []

        for i in range(POP_SIZE):
'''
