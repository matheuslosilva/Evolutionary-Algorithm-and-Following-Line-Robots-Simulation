import pygame
import sys
from constants import WIDTH, HEIGHT
from simulationclass import Simulation


# Environment init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 3)
show = True # Flag to indicate whether the simulation will present the visual part or not

simulation = Simulation()

################################################################################
# Main loop
running = True
while running:
    screen.fill((50, 120, 40))
    
    # A faster loop to run AE faster when a visualization is off
    while (not show):
    	simulation.run()
    	for event in pygame.event.get():
	        if event.type == pygame.KEYUP:
	            if event.key in [pygame.K_SPACE]:
	                show = not show


    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False 

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:# Press Space to turn off the visual simulation
                show = not show

    # To make the simulation run faster, the visual part can be turned off, thus, the fps will no longer be limited
    if show:	
    	FPS = 60 # Frame updates per second
    	simulation.show(screen)
    else: FPS = 10000000
    pygame.display.update()
    clock.tick(FPS)
################################################################################

# End
pygame.quit()
sys.exit()