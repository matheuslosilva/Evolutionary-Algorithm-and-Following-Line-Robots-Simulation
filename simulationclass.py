from evolutiveclass import Evolutive, POP_SIZE
from trackclass import Track, trackVertices

class Simulation:
    def __init__(self):
        self.track = Track(trackVertices[0])
        self.evolutive = Evolutive()
        self.curRobot = self.evolutive.robotInit(self.track, 0)

        # Robot evaluation parameters
        self.curRobotIndex = 0

        # Lose points
        self.robotFailed = False
        self.didRobotLeftTrack = False
        self.isRobotInLoop = False
        self.didRobotMissCourse = False
        self.curRobotIterations = 0

        # Earn points 
        self.robotCompleteCourse = False # TODO
        self.curRobotCheckpointsReached = 0
        self.curRobotCompleteLaps = 0

        # Group of the robot's actions to evolutive evaluate function 
        self.curRobotReport = {
            "robotLeftTrack" : 0,
            "robotInLoop" : 0,
            "robotMissCourse" : 0,
            "robotIterations" : 0,
            "completeCourse" : 0,
            "completeLaps" : 0,
            "reachedCheckpoints" : 0    
        }

    def fillRobotReport(self):
        if not self.didRobotLeftTrack: 
            self.curRobotReport["robotLeftTrack"] = 1
        if self.didRobotInLoop: 
            self.curRobotReport["robotInLoop"] = 1
        if self.didRobotMissCourse: 
            self.curRobotReport["robotMissCourse"] = 1
        self.curRobotReport["robotIterations"] = self.curRobotIterations        
        
        if self.robotCompleteCourse: 
            self.curRobotReport["completeCourse"] = 1
        self.curRobotReport["completeLaps"] = self.curRobotCompleteLaps 
        self.curRobotReport["reachedCheckpoints"] = self.curRobotCheckpointsReached  
    
    def run(self):
        # Move Robot
        self.curRobot.updateLineSensorsPosition(self.track)
        self.curRobot.move()

        # Update evaluation report parameters
        self.didRobotLeftTrack = self.curRobot.checkIsOnTheTrack(self.track)
        self.didRobotInLoop = self.curRobot.checkRobotInLoop()
        self.didRobotMissCourse = self.curRobot.checkMissCourse()
        self.robotCompleteCourse = self.curRobot.checkCompleteCourse()

        # Checks if the robot is on the track in it's course
        if not self.didRobotLeftTrack:
            self.robotFailed = True
            print("Out of the Track") # TODO create a print metod

        # Checks if the robot has entered a loop
        elif self.didRobotInLoop:
            self.robotFailed = True
            print("robot has entered in a loop")

        # Checks if the robot has missed the course
        elif self.didRobotMissCourse:
            self.robotFailed = True
            print("robot missed the course")


        if self.robotFailed or self.robotCompleteCourse:
            # Update the number of iterations, checkpoints and laps made by the robot on the course
            self.curRobotIterations = self.curRobot.iterations
            self.curRobotCheckpointsReached = self.curRobot.numberCheckpointsReached
            self.curRobotCompleteLaps = self.curRobot.completeLaps

            self.fillRobotReport()

            self.evolutive.evaluateRobotFitness(self.curRobotIndex, self.curRobotReport)

            self.robotFailed = False
            self.robotCompleteCourse = False
            self.curRobotIndex += 1
             
            if self.curRobotIndex == POP_SIZE:
                print(self.evolutive.fitnessPop) 
                self.curRobotIndex = 0 # TODO evolutive part of the simulation here

            self.curRobot = self.evolutive.robotInit(self.track, self.curRobotIndex)

    def show(self, screen): 
        self.run()
        self.track.show(screen)
        self.curRobot.show(screen)