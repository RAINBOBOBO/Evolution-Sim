import sys
import pygame
from pygame.locals import *
import os
import numpy as np
import neat
from abc import ABC, abstractmethod
from fractions import Fraction
import mainsim
from mainsim import *
import math

# import tensorflow as tf
# from tensorflow.keras import layers
# import keras

pygame.init()

# 0=null
# 1='water'
# 2='creature'
# 3='food'
# 4=out of bounds

size = width, height = 1300, 1080
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
white = [255, 255, 255]

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
screen = pygame.display.set_mode(size, pygame.NOFRAME)
myFont = pygame.font.SysFont("arial", 15)
maxX = maxY = 30

maxTime = 30
sightLim = 3  # the hard cap, in matrix units (MU's now) of how far someone can see
clock = pygame.time.Clock()
FPS = 60
seed = 15
np.random.seed(seed)

matrix = matrix(maxX, maxY, maxTime)

foodCount = 10
for x in range(foodCount):
    temp = food(np.random.randint(0, maxX), np.random.randint(0, maxY))
    matrix.foods.append(temp)

creatureTagGenerator = creatureTagger()
creatureCount = 10
for x in range(creatureCount):
    tempCreature = creature(creatureTagGenerator.get_tag(), 1, 0, 1, 1, None, np.random.randint(0, 1001), np.random.randint(10, 101), np.random.randint(0, maxX), np.random.randint(0, maxY))
    matrix.creatures.append(tempCreature)

#loading into matrix
for foodloader in range(foodCount):
    matrix.matrix[matrix.foods[foodloader].get_Pos()[0], matrix.foods[foodloader].get_Pos()[1], 0] = matrix.foods[foodloader]

for creatureLoader in range(creatureCount):
    if type(matrix.matrix[matrix.creatures[creatureLoader].x, matrix.creatures[creatureLoader].y, 0]) == mainsim.food:
        print("creature ate at ", matrix.creatures[creatureLoader].x, matrix.creatures[creatureLoader].y)
        matrix.creatures[creatureLoader].add_food()
        matrix.eat(matrix.foods, (matrix.creatures[creatureLoader].x, matrix.creatures[creatureLoader].y))
        foodCount -= 1
    matrix.matrix[matrix.creatures[creatureLoader].x, matrix.creatures[creatureLoader].y, 0] = matrix.creatures[creatureLoader]

state = 1
while state == 1:  # sim
    for time in range(maxTime-1):

        for fooder in matrix.foods:
            matrix.matrix[fooder.get_Pos()[0], fooder.get_Pos()[1], time + 1] = matrix.matrix[fooder.get_Pos()[0], fooder.get_Pos()[1], time]

        for creer in matrix.creatures:
            decisionX = dec()
            decisionY = dec()
            xDist = 0
            yDist = 0
            if decisionX == 0:
            	xDist += creer.speed
            elif decisionX == 1:
            	xDist -= creer.speed
            if decisionY == 0:
            	yDist += creer.speed
            elif decisionY == 1:
            	yDist -= creer.speed
            matrix.move_Check(creer, xDist, yDist, time)

    state = 2

matrix.show_Matrix(size[0], size[1], maxTime)