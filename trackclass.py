import pygame
import pygame.gfxdraw
    

trackVertices = [[        
    (100, 150), (300, 150), (300, 300), (500, 300),
    (500, 150), (600, 100), (700, 150), (700, 300), 
    (900, 300), (900, 450), (750, 450), (750, 600),
    (550, 600), (550, 450), (400, 450), (400, 550),
    (300, 600), (200, 550), (200, 300), (100, 300) 
    ], []]

class Track:
    def __init__(self, vertices):
        self.vertices = vertices

        # Create a new surface to check if the robot in on the track
        self.newSurface = pygame.Surface((1000,700))
        self.newSurface.fill((255, 255, 255))
        self.show(self.newSurface)

    def show(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 5)

    def isPointInTrack(point, track):
        # Check whether the spot on the surface is black (track) or not
        return pygame.surfarray.pixels2d(track.newSurface)[round(point[0])][round(point[1])] == 0