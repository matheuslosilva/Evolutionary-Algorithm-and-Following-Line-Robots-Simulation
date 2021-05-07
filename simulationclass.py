from evolutiveclass import Evolutive
from trackclass import Track, trackVertices

class Simulation:
    
    def __init__(self):
        self.track = Track(trackVertices)
        self.evolutive = Evolutive()
        self.curRobot = self.evolutive.robotInit(self.track, 0)

        # Robot evaluation parameters
        self.curRobotIndex = 0
        self.robotFailed = False
        self.completeCourse = False # TODO

        self.checkpoints = self.track.vertices
        self.isRobotOnTrack = True
        self.isRobotInLoop = False
        self.didRobotMissCourse = False

    def run(self):
        self.curRobot.updateLineSensorsPosition(self.track)
        self.curRobot.move()
        self.isRobotOnTrack = self.curRobot.isOnTheTrack(self.track)
        self.isRobotInLoop = self.curRobot.checkRobotInLoop()
        self.didRobotMissCourse = self.curRobot.checkMissCourse()

        # Checks if the robot is on the track in it's course
        if not self.isRobotOnTrack:
            self.robotFailed = True
            print("Out of the Track")

        # TODO Checks if the robot has missed the course
        elif self.isRobotInLoop:
            self.robotFailed = True
            print("robot has entered in a loop")

        # Checks if the robot has entered a loop
        elif self.didRobotMissCourse:
            self.robotFailed = True
            print("robot missed the course")

        if self.robotFailed:
            self.robotFailed = False
            self.curRobotIndex += 1
            if self.curRobotIndex == 30: self.curRobotIndex = 0 # TODO evolutive part of the simulation here
            self.curRobot = self.evolutive.robotInit(self.track, self.curRobotIndex)


    def show(self, screen): 
    	self.run()
    	self.track.show(screen)
    	self.curRobot.show(screen)