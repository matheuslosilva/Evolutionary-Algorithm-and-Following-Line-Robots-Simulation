import pygame
import sys
from constants import WIDTH, HEIGHT

from simulationclass import Simulation
from trackclass import Track, trackVertices


pygame.init()

# Screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))

################################################################################
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 3)

#Simulation Init
simulation = Simulation(Track(trackVertices))

################################################################################

show = True

# Main loop
running = True
while running:
    # Reset screen
    screen.fill((50, 120, 40))

    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False 

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:# Press Space to turn off the visual simulation
                show = not show

    simulation.run()

    # Clock tick
    # To make the simulation run faster, the visual part can be turned off
    FPS = 10000
    if show:
    	# Frame updates per second
    	FPS = 500
    	simulation.show(screen)
    pygame.display.update()
    clock.tick(FPS)

################################################################################

# End
pygame.quit()
sys.exit()