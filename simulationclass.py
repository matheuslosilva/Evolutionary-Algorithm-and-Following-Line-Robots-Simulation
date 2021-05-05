import pygame

from robotclass import Robot
from random import randint, choice
from time import time
from evolutiveclass import Evolutive

import math

class Simulation:
    def __init__(self, track):
        self.track = track
        self.evolutive = Evolutive(1)
        lineSensors = self.evolutive.sensorInit()
        self.robot = Robot(track.vertices[0], lineSensors)        

    def run(self):
        self.robot.updateLineSensorsPosition(self.track)
        self.robot.move()

    def show(self, screen):      
        self.robot.isOnTheLine(self.track)
        self.track.show(screen)
        self.robot.show(screen)