from constants import FORWARD, RIGHT, LEFT, SENSORS_NUMBER
from robotclass import Robot, LineSensor
from random import randint, seed, sample
import math

# TODO evolutive algorithm
RANDOM_SEED = 123456645
POP_SIZE = 40
CROSSOVER_RATE = 70
MUTATION_RATE = 3

# Evaluation constants
LEFT_TRACK_LOST_POINTS = -300
LOOP_LOST_POINTS = -500
MISS_COURSE_LOST_POINTS = -200
ITERATIONS_NUMBER_LOST_POINTS = -0.30
COMPLETE_COURSE_EARNED_POINTS = 10000
CHECKPOINTS_NUMBER_EARNED_POINTS = 150
LAPS_NUMBER_EARNED_POINTS = 200


class Evolutive:
    def __init__(self):
        seed(RANDOM_SEED)

        self.population = self.popInit()
        self.fitnessPop = [0 for _ in range(POP_SIZE)] # Stores all the fitness of the population's robots

    def setIndividualSensors(self, newChromossome): 

        if newChromossome != 0:      
            # Create random positions for the robot's line sensors
            fSensor = LineSensor((0, 0, 255), 3, FORWARD, newChromossome[0]) # Forward sensor
            lSensor = LineSensor((0, 0, 255), 3, LEFT, newChromossome[1]) # Left sensor
            rSensor = LineSensor((0, 0, 255), 3, RIGHT, newChromossome[2]) # Right sensor
        else:
            # Create random positions for the robot's line sensors
            fSensor = LineSensor((0, 0, 255), 3, FORWARD, (randint(-15, 40), randint(-5, 5))) # Forward sensor
            lSensor = LineSensor((0, 0, 255), 3, LEFT, (randint(-40, 40), randint(-40, 40))) # Left sensor
            rSensor = LineSensor((0, 0, 255), 3, RIGHT, (randint(-40, 40), randint(-40, 40))) # Right sensor      
      
        return [fSensor, lSensor, rSensor]

    def popInit(self):
        population = []
        
        for p in range(POP_SIZE):
            individual = self.setIndividualSensors(0)
            population.append(individual)

        # Inserts a good robot in the population to check if the evolutionary algorithm its working and converging
        '''fSensor = LineSensor((0, 0, 255), 3, FORWARD, (15,-5)) # Forward sensor
        lSensor = LineSensor((0, 0, 255), 3, LEFT, (14,-7)) # Left sensor
        rSensor = LineSensor((0, 0, 255), 3, RIGHT, (10,7)) # Right sensor   

        population.append([fSensor, lSensor, rSensor])'''
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
        print(fitness)
        self.fitnessPop[curRobotIndex] += fitness

    def getBestRobotIndex(self):
        maxFitness = self.fitnessPop[0]
        maxFitnessIndex = 0

        for i in range(len(self.fitnessPop)):
            if self.fitnessPop[i] > maxFitness:
                maxFitnessIndex = i
                maxFitness = self.fitnessPop[i]

        print(maxFitness)
        return maxFitnessIndex

    def mutation(self, chromossome):
        newChromossome = []

        for i in range(SENSORS_NUMBER):
            if randint(1,100) <= MUTATION_RATE:
                xCoord = randint(-40, 40)
            else:
                xCoord = chromossome[i][0]   

            if randint(1,100) <= MUTATION_RATE:
                yCoord = randint(-40, 40)
            else:
                yCoord = chromossome[i][1]

            newChromossome.append((xCoord, yCoord))

        return newChromossome

    def crossover(self, individualsSelected):
        bestIndividual = self.population[individualsSelected[0]]
        secondBestIndividual = self.population[individualsSelected[1]]

        newChromossome = []

        for i in range(SENSORS_NUMBER):
            bestCoord = bestIndividual[i].coordRelativeRobot
            childCoord = secondBestIndividual[i].coordRelativeRobot

            if randint(0, 100) < CROSSOVER_RATE:
                # Weighted average Crossover, brings the "child's" chromossome closer to the "parent's" chromossome
                # based on a percentage of the difference between its values
                xCoord = math.floor(childCoord[0] + (randint(0, 100)/100)*(bestCoord[0]-childCoord[0]))
                yCoord = math.floor(childCoord[1] + (randint(0, 100)/100)*(bestCoord[1]-childCoord[1]))
            else:
                xCoord = childCoord[0]
                yCoord = childCoord[1]

            newChromossome.append((xCoord, yCoord))
        
        return newChromossome

    def newPopulation(self):
        '''for i in range(POP_SIZE): 
            print(self.population[i][0].coordRelativeRobot, self.population[i][1].coordRelativeRobot, self.population[i][2].coordRelativeRobot)
        print(self.fitnessPop)'''
        print(self.fitnessPop[self.getBestRobotIndex()])

        bestIndividual = self.getBestRobotIndex()
        newPopulation = []
        newChromossome = []
        newIndividual = []
        
        # Elitism selection, the best individual will cross its genes with everyone elsae
        for i in range(POP_SIZE-1):
            newChromossome = self.crossover((bestIndividual, i))
            newChromossome = self.mutation(newChromossome)

            newIndividual = self.setIndividualSensors(newChromossome)
            newPopulation.append(newIndividual)

        newPopulation.append(self.population[bestIndividual]) 
        self.population = newPopulation

    '''
    # Another selection method that is used to mantain a greater genetic variability
     def tournament2Selection(self):
        indexCompetitor1 = randint(0, (POP_SIZE - 1))
        indexCompetitor2 = randint(0, (POP_SIZE - 1))

        indexCompetitor3 = randint(0, (POP_SIZE - 1))
        indexCompetitor4 = randint(0, (POP_SIZE - 1))
        
        selectedIndexToCrossover = []

        if self.fitnessPop[indexCompetitor1] >= self.fitnessPop[indexCompetitor2]:
            selectedIndexToCrossover.append(indexCompetitor1)
        else:
            selectedIndexToCrossover.append(indexCompetitor2)

        if self.fitnessPop[indexCompetitor3] >= self.fitnessPop[indexCompetitor4]:
            selectedIndexToCrossover.append(indexCompetitor3)
        else:
            selectedIndexToCrossover.append(indexCompetitor4)
        
        return selectedIndexToCrossover
    '''