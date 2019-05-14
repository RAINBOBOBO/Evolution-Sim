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


# NEAT TESTING

parent1 = Genome()
for i in range(3):
    node = NodeGene(0, i+1)
    parent1.addNodeGene(node)
parent1.addNodeGene(NodeGene(1, 4))
parent1.addNodeGene(NodeGene(2, 5))

parent1.addConnectionGene(ConnectionGene(1, 4, float(1), True, 1))
parent1.addConnectionGene(ConnectionGene(2, 4, float(1), False, 2))
parent1.addConnectionGene(ConnectionGene(3, 4, float(1), True, 3))
parent1.addConnectionGene(ConnectionGene(2, 5, float(1), True, 4))
parent1.addConnectionGene(ConnectionGene(5, 4, float(1), True, 5))
parent1.addConnectionGene(ConnectionGene(1, 5, float(1), True, 8))

parent2 = Genome()
for i in range(3):
    node = NodeGene(0, i+1)
    parent2.addNodeGene(node)
parent2.addNodeGene(NodeGene(1, 4))
parent2.addNodeGene(NodeGene(2, 5))
parent2.addNodeGene(NodeGene(2, 6))

parent2.addConnectionGene(ConnectionGene(1, 4, float(1), True, 1))
parent2.addConnectionGene(ConnectionGene(2, 4, float(1), False, 2))
parent2.addConnectionGene(ConnectionGene(3, 4, float(1), True, 3))
parent2.addConnectionGene(ConnectionGene(2, 5, float(1), True, 4))
parent2.addConnectionGene(ConnectionGene(5, 4, float(1), False, 5))
parent2.addConnectionGene(ConnectionGene(5, 6, float(1), True, 6))
parent2.addConnectionGene(ConnectionGene(6, 4, float(1), True, 7))
parent2.addConnectionGene(ConnectionGene(3, 5, float(1), True, 9))
parent2.addConnectionGene(ConnectionGene(1, 6, float(1), True, 10))

child = parent1.crossover(parent2, parent1)

state = 3

showGenome2(child)
pygame.display.flip()
while state == 3:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()