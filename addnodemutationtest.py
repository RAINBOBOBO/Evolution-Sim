import sys
import pygame
import os
import numpy as np

import mainsim
from mainsim import *

pygame.init()

size = width, height = 500, 500
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
white = [255, 255, 255]

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
screen = pygame.display.set_mode(size, pygame.NOFRAME)
clock = pygame.time.Clock()
FPS = 60
seed = 57
np.random.seed(seed)

innovation = InnovationGenerator()
genome = Genome()

input1 = NodeGene(0, 1)
input2 = NodeGene(0, 2)
output = NodeGene(1, 3)

con1 = ConnectionGene(1, 3, float(1), True, innovation.get_innovation())
con2 = ConnectionGene(2, 3, float(1), True, innovation.get_innovation())

genome.addNodeGene(input1)
genome.addNodeGene(input2)
genome.addNodeGene(output)

genome.addConnectionGene(con1)
genome.addConnectionGene(con2)

genome.addNodeMutation(innovation)

showGenome2(genome)

state = 3
pygame.display.flip()
while state == 3:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()