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
maxX = 10
maxY = 10
maxTime = 60
world = np.full((maxX, maxY, maxTime), 1)
sightLim = 3  # the hard cap, in matrix units (MU's now) of how far someone can see
clock = pygame.time.Clock()
FPS = 60
seed = 57
np.random.seed(seed)

food1Count = np.random.randint(2, 4)
foodlist = []

for food1Maker in range(food1Count):
    tempfood1 = food1(np.random.randint(0, 10), np.random.randint(0, 10))
    foodlist.append(tempfood1.getPos())

hazard1Count = np.random.randint(1, 3)
hazardlist = []

for hazard1Maker in range(hazard1Count):
    temphazard1 = hazard1(np.random.randint(0, 10), np.random.randint(0, 10))
    hazardlist.append(temphazard1.getPos())

creatureCount = np.random.randint(1, 3)
creaturelist = []

for creatureMaker in range(creatureCount):
    tempCreBod = node(None, None, None, None,np.random.randint(0, 10), np.random.randint(0, 10))
    tempCre = creature(tempCreBod, 1, 0, 1, 2, None)
    creaturelist.append(tempCre)

hCounter = 0
hlist = []
fCounter = 0
flist = []

for col1 in range(food1Count):
    for col2 in range(hazard1Count):
        decider = np.random.randint(1, 3)
        if (hazardlist[col2] == foodlist[col1]):
            if decider == 1:
                hCounter += 1
                hlist.append(hazardlist[col2])
                hazard1Count -= 1
                print("collision detected 1")
            else:
                fCounter += 1
                flist.append(foodlist[col1])
                food1Count -= 1
                print("collision detected 2")

if hCounter > 0:
    for hdel in range(hCounter):
        eat(hazardlist, hlist[hdel])
        print("collision resolved 1")

if fCounter > 0:
    for fdel in range(fCounter):
        eat(foodlist, flist[fdel])
        print("collision resolved 2")

# LOADING INTO MATRIX

for foodloader in range(food1Count):
    world[foodlist[foodloader][0], foodlist[foodloader][1], 0] = 3

for hazardloader in range(hazard1Count):
    world[hazardlist[hazardloader][0], hazardlist[hazardloader][1], 0] = 4

for creatureloader in range(creatureCount):
    if world[creaturelist[creatureloader].Body1.getX(), creaturelist[creatureloader].Body1.getY(), 0] == 3:
        print("creature eaten!")
        creaturelist[creatureloader].add_food()
        eat(foodlist, (creaturelist[creatureloader].Body1.getX(), creaturelist[creatureloader].Body1.getY()))
        food1Count -= 1
    elif world[creaturelist[creatureloader].Body1.getX(), creaturelist[creatureloader].Body1.getY(), 0] == 4:
        print("creature eaten -_-")
        creaturelist[creatureloader].add_health(-1)
        eat(hazardlist, (creaturelist[creatureloader].Body1.getX(), creaturelist[creatureloader].Body1.getY()))
        hazard1Count -= 1
    world[creaturelist[creatureloader].Body1.getX(), creaturelist[creatureloader].Body1.getY(), 0] = 2

state = 2

t = 0

#print(foodlist, " | ", hazardlist)
#print("===============")

# put everything in another while loop so that you don't have to use goto

while state == 1:  # sim

    for time in range(maxTime - 1):

        for fooder in range(food1Count):
            tempPos = foodlist[fooder]
            world[tempPos[0], tempPos[1], time + 1] = world[tempPos[0], tempPos[1], time]

        for hazer in range(hazard1Count):
            tempPos = hazardlist[hazer]
            world[tempPos[0], tempPos[1], time + 1] = world[tempPos[0], tempPos[1], time]

        for creer in range(creatureCount):
            if creaturelist[creer].get_health() > 0:
                eatType = dec(creaturelist[creer], world, time, foodlist, hazardlist)
                if eatType == 3:
                    food1Count -= 1
                elif eatType == 4:
                    hazard1Count -= 1
                    print(foodlist, " | ", hazardlist)
                    foodadder = [creaturelist[creer].Body1.getX(), creaturelist[creer].Body1.getY()]
                    foodlist.append(foodadder)
                    food1Count += 1
                    print(foodlist, " | ", hazardlist)
    state = 2

while state == 2:  # viewer

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()
        if key[pygame.K_p]:
            if t < (maxTime - 1):
                t += 1
                print("t = ", t)
        if key[pygame.K_o]:
            if t > 0:
                t -= 1
                print("t = ", t)
        # if bob.health > 0:
        #    if key[pygame.K_SPACE]:
        #        copier = bob.get_vis(world, t)
        #        print(copier)
        #        visual = bob.process_vis(copier)
        #        print(visual)
        # keep this as a template

    for x in range(10):
        for y in range(10):
            if world[x, y, t] == 1:
                pygame.draw.rect(screen, blue, (50 * x, 50 * y, 50, 50))
            elif world[x, y, t] == 2:
                pygame.draw.rect(screen, yellow, (50 * x, 50 * y, 50, 50))
            elif world[x, y, t] == 3:
                pygame.draw.rect(screen, green, (50 * x, 50 * y, 50, 50))
            elif world[x, y, t] == 4:
                pygame.draw.rect(screen, red, (50 * x, 50 * y, 50, 50))

    pygame.display.flip()