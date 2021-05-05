import math
import pygame

from trackclass import Track
from constants import FORWARD, RIGHT, LEFT

class Sensor:
    def __init__(self, coordRelativeRobot, direction, color):
        self.coord = coordRelativeRobot
        self.position = (0,0)
        self.direction = direction
        self.color = color
        
        
class Robot:
    def __init__(self, center, lineSensors):
        self.center = center

        self.theta = math.pi/2
        self.dTheta = 8

        self.velocity = 4
        self.direction = 0

        self.numberEdgeSensors = 100
        self.edgeRadius = 25
        self.edgeSensors = []

        self.lineSensors = lineSensors

    def move(self):
        if self.direction == FORWARD:
            x = self.center[0] + math.cos(self.theta) * self.velocity
            y = self.center[1] + math.sin(self.theta) * self.velocity
            
            self.center = (x, y)
       
        elif self.direction == LEFT:
            self.theta -= self.dTheta * ((2*math.pi)/360)

        elif self.direction == RIGHT:
            self.theta += self.dTheta* ((2*math.pi)/360)

    def updateLineSensorsPosition(self, track):
        for sensor in self.lineSensors:
            # Calculates the position of the sensor relative to the center of the robot, with the coordinates of the sensor
            x = sensor.coord[0]*math.cos(self.theta) - sensor.coord[1]*math.sin(self.theta) + self.center[0]
            y = sensor.coord[0]*math.sin(self.theta) + sensor.coord[1]*math.cos(self.theta) + self.center[1]
            sensor.position = (x,y)
            self.detectLineSensors(sensor, track)

    def detectLineSensors(self, sensor, track):
        if Track.isPointInTrack(sensor.position, track):
            self.direction = sensor.direction
        
    def updateEdgeSensorPosition(self, p):
        theta = p * (360 / self.numberEdgeSensors) * (math.pi / 180)
        # Calculates the position of the border sensor relative to the robot, with the distance of a radius in relation to the center     
        x = self.center[0] + math.cos(theta) * self.edgeRadius
        y = self.center[1] + math.sin(theta) * self.edgeRadius

        return (x, y)
    

    def isOnTheLine(self, track):
        isOnTheTrack = False;
        updatedLineSensors = []

        sensorXY = []
        # Creates a sensor border around the robot to verify that it is on the track
        for p in range(self.numberEdgeSensors):
            sensorXY = self.updateEdgeSensorPosition(p)

            if Track.isPointInTrack(sensorXY, track):
                newColor = (255, 25, 25)
                updatedLineSensors.append((sensorXY, newColor))

                isOnTheTrack = True;
            else:
                newColor = (255, 255, 25)
                updatedLineSensors.append((sensorXY, newColor))

        self.edgeSensors = updatedLineSensors

    def show(self, screen):
        headLength = 30
        baseLength = 30
        halfBaseLength = baseLength // 2

        x = self.center[0] + math.cos(self.theta) * headLength
        y = self.center[1] + math.sin(self.theta) * headLength

        pygame.draw.line(screen, (255, 25, 25), self.center, (x, y), 1)

        m = -1/math.tan(self.theta)
        x1 = self.center[0] + math.cos(self.theta + math.pi/2) * halfBaseLength
        y1 = self.center[1] + math.sin(self.theta + math.pi/2) * halfBaseLength

        x2 = self.center[0] + math.cos(self.theta - math.pi/2) * halfBaseLength
        y2 = self.center[1] + math.sin(self.theta - math.pi/2) * halfBaseLength
        pygame.draw.line(screen, (25, 255, 25), (x1, y1), (x2, y2), 1)

        for (x, y), color in self.edgeSensors:
            pygame.draw.circle(screen, color, (x, y), 1, 1)

        for sensor in self.lineSensors:
            pygame.draw.circle(screen, sensor.color, (sensor.position[0], sensor.position[1]), 3, 3)