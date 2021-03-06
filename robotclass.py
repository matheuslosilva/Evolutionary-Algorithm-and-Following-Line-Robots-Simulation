import math
import pygame
from trackclass import Track
from constants import FORWARD, RIGHT, LEFT, LOOP_ITERATIONS_LIMIT, NUMBER_OF_LAPS_IN_A_COURSE


class Sensor:
    def __init__(self, color, radius):
        self.position = (0,0)
        self.color = color
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def detectLine(self, track):
        return track.isPointInTrack(self.position)

class BorderSensor(Sensor):
    def __init__(self, color, radius, totalNumberEdgeSensors, sensorIndex):
        super().__init__(color, radius)
        self.theta = sensorIndex * (360 / totalNumberEdgeSensors) * (math.pi / 180)

    def updatePositionRelativeRobot(self, centerRobot, edgeRadius):
        # Calculates the position of the border sensor relative to the robot, with the distance of a radius in relation to the center     
        x = centerRobot[0] + math.cos(self.theta) * edgeRadius
        y = centerRobot[1] + math.sin(self.theta) * edgeRadius
        self.position = (x,y)

class LineSensor(Sensor):
    def __init__(self, color, radius, direction, coordRelativeRobot):
        super().__init__(color, radius)
        self.directionMoveRobot = direction
        self.coordRelativeRobot = coordRelativeRobot

    def updatePositionRelativeRobot(self, centerRobot, theta):
        # Calculates the position of the sensor relative to the center of the robot, with the coordinates of the sensor
        x = self.coordRelativeRobot[0]*math.cos(theta) - self.coordRelativeRobot[1]*math.sin(theta) + centerRobot[0]
        y = self.coordRelativeRobot[0]*math.sin(theta) + self.coordRelativeRobot[1]*math.cos(theta) + centerRobot[1]
        self.position = (x,y)
        
class Robot:
    def __init__(self, startingPosition, lineSensors, checkpoints):
        # Initiation parameters
        self.center = startingPosition
        self.lineSensors = lineSensors
        self.checkpointsToReach = checkpoints    

        # Movement parameters
        self.theta = 0
        self.dTheta = 5
        self.velocity = 4
        self.direction = RIGHT

        # Parameters for robot evalutaion:
        # -Track proximity sensor
        self.numberEdgeSensors = 50
        self.edgeRadius = 30 
        self.edgeSensors = [BorderSensor((255, 255, 25), 1, self.numberEdgeSensors, i+1) for i in range(self.numberEdgeSensors)]

        # -Evaluate the course of the robot
        self.numberCheckpointsReached = 0
        self.penultimateCheckpointReached = self.checkpointsToReach[len(self.checkpointsToReach)-1] # Parameter to check if the robot is on a wrong course
        self.nextCheckpointToReach = self.checkpointsToReach[self.numberCheckpointsReached]
        self.completeLaps = 0

        # -Looping Check:
        self.iterations = 0 # The iteration's number will simulate the time it took the robot to complete its course
        self.loopIterationsCounter = 0

    def checkpointReached(self):
        x0 = self.center[0]
        y0 = self.center[1]
        x1 = self.nextCheckpointToReach[0]
        y1 = self.nextCheckpointToReach[1]

        # Check colision of the robot and the checkpoints and update checkpoints variables
        if ((x1 - x0)**2 + (y1 - y0)**2 <= (self.edgeRadius+15)**2):
            if self.numberCheckpointsReached > 1:
                self.penultimateCheckpointReached =  self.checkpointsToReach[self.numberCheckpointsReached - 2]
            self.numberCheckpointsReached += 1

            # If only 1 checkpoint is missing
            if self.numberCheckpointsReached == len(self.checkpointsToReach):
                self.nextCheckpointToReach = self.checkpointsToReach[0]

            # If the robot complete a lap
            elif self.numberCheckpointsReached == (len(self.checkpointsToReach) + 1):
                self.completeLaps += 1

                self.numberCheckpointsReached = 0
                self.penultimateCheckpointReached = self.checkpointsToReach[len(self.checkpointsToReach)-1]
                self.nextCheckpointToReach = self.checkpointsToReach[self.numberCheckpointsReached]

            else:
                self.nextCheckpointToReach = self.checkpointsToReach[self.numberCheckpointsReached]

            return True

        return False

    def move(self):
        if self.direction == FORWARD:
            x = self.center[0] + math.cos(self.theta) * self.velocity
            y = self.center[1] + math.sin(self.theta) * self.velocity            
            self.center = (x, y)

        elif self.direction == LEFT:
            self.theta -= self.dTheta * ((2*math.pi)/360)

        elif self.direction == RIGHT:
            self.theta += self.dTheta* ((2*math.pi)/360)

        self.iterations += 1

    def updateLineSensorsPosition(self, track):
        for sensor in self.lineSensors:
            sensor.updatePositionRelativeRobot(self.center, self.theta)
            # Change the movement direction of the robot according to the sensor reading            
            if sensor.detectLine(track):
                self.direction = sensor.directionMoveRobot 

    def checkIsOnTheTrack(self, track):
        isOnTheTrack = False;
        # Iterates through all the border sensors around the robot to check if it is on the track

        for sensor in self.edgeSensors:
            sensor.updatePositionRelativeRobot(self.center, self.edgeRadius)
            if sensor.detectLine(track):
                sensor.color = (255, 25, 25)
                isOnTheTrack = True;
            else: 
                sensor.color = (255, 255, 25)
        return isOnTheTrack

    def checkRobotInLoop(self):
        self.loopIterationsCounter += 1

        if self.checkpointReached():
            self.loopIterationsCounter = 0
        elif self.loopIterationsCounter > LOOP_ITERATIONS_LIMIT:
            return True
        
        return False

    def checkMissCourse(self):
        x0 = self.center[0]
        y0 = self.center[1]
        x1 = self.penultimateCheckpointReached[0]
        y1 = self.penultimateCheckpointReached[1]

        # Check colision of the robot and the penultimate checkpoint
        if ((x1 - x0)**2 + (y1 - y0)**2 <= self.edgeRadius**2):
            return True

        return False

    def checkCompleteCourse(self):
        if self.completeLaps == NUMBER_OF_LAPS_IN_A_COURSE:
            return True
        else:
            return False

    def show(self, screen):
        headLength = 25
        baseLength = 40
        halfBaseLength = baseLength / 2

        baseX = math.cos(self.theta) * -headLength + self.center[0] 
        baseY = math.sin(self.theta) * -headLength + self.center[1]

        x = math.cos(self.theta) * headLength + self.center[0] 
        y = math.sin(self.theta) * headLength + self.center[1]
        x1 = math.cos(self.theta + math.pi/2) * halfBaseLength + baseX
        y1 = math.sin(self.theta + math.pi/2) * halfBaseLength + baseY
        x2 = math.cos(self.theta - math.pi/2) * halfBaseLength + baseX
        y2 = math.sin(self.theta - math.pi/2) * halfBaseLength + baseY

        pygame.draw.polygon(screen, (1, 1, 1), ((x,y),(x1,y1),(x2,y2)), 2)

        for sensor in self.edgeSensors:
            sensor.draw(screen)

        for sensor in self.lineSensors:
            sensor.draw(screen)