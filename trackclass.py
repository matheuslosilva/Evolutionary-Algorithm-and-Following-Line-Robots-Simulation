import pygame
import constants
	
trackVertices = [        
	(100,150), (300,150), (300,300), (450,300),
    (450,150), (600, 50), (750,150), (750,300), 
    (900,300), (900,450), (750,450), (750,600),
    (550,600), (550,450), (400,450), (400,550),
    (300,650), (200,550), (200,300), (100,300) 
    ]


class Track:
    def __init__(self, vertices):
        self.vertices = vertices
        self.newSurface = pygame.Surface((1000,700))
        self.newSurface.fill((255, 255, 255))
        self.show(self.newSurface)

    def show(self, screen):
        pygame.draw.polygon(screen, (0, 0, 0), self.vertices, 5)

    def isPointInTrack(point, track):
        return pygame.surfarray.pixels2d(track.newSurface)[round(point[0])][round(point[1])] == 0