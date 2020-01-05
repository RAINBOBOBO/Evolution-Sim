import sys
import pygame
import os
import numpy as np
import neat
from abc import ABC, abstractmethod
from fractions import Fraction
import math

# import tensorflow as tf
# from tensorflow.keras import layers
# import keras

pygame.init()

# 0=null
# 1=water
# 2=creature
# 3=food
# 4=out of bounds

black = [0, 0, 0]
red = [200, 0, 0]
green = [0, 200, 0]
light_green = [0, 255, 0]
blue = [0, 0, 200]
yellow = [255, 255, 0]
white = [255, 255, 255]

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
myFont = pygame.font.SysFont("arial", 15)
sightLim = 3  # the hard cap, in matrix units (MU's now) of how far someone can see
clock = pygame.time.Clock()
FPS = 60
seed = 5
screenSizeY = 1080
screenSizeX = 1920
np.random.seed(seed)


def dec():
    num = np.random.randint(0, 3)
    return num

def partition(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   arr[j] <= pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)

def thousandCircle(num):
    #change any number into a number from 1-1000 where 1000+1=1 and 1-1=1000
    if num > 1000:
        newNum = num % 1000
        return newNum
    else:
        return num

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

class water():
    def __init__(self):
        pass

class void():
    def __init__(self):
        pass

class food():
    def __init__(self, x, y, edibility = None):
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.edibility = edibility

    def get_Pos(self):
        return self.pos

class creature():
    def __init__(self, tag = None, speed = None, food = None, health = None, sight = None, actionPoints = None, digestibility = None, digestRange = None, x = None, y = None):
        self.tag = tag
        self.speed = speed
        self.food = food
        self.health = health
        self.sight = sight
        self.actionPoints = actionPoints
        self.digestibility = digestibility
        self.digestRange = digestRange
        self.x = x
        self.y = y

    def get_Body(self):
        return self

    def get_speed(self):
        return self.speed

    def get_food(self):
        return self.food

    def get_health(self):
        return self.health

    def get_sight(self):
        return self.sight

    def get_actionPoints(self):
        return self.actionPoints

    def moveX(self, amt = None):
        if (amt):
            self.x += amt
        else:
            self.x += 1

    def moveY(self, amt = None):
        if (amt):
            self.y += amt
        else:
            self.y += 1

    def add_food(self, amt = None): #make this depend on the digestibility and edibility
        if amt != None:
            self.food += amt
        else:
            self.food += 1

    def add_health(self, amt = None):
        if amt != None:
            self.health += amt
        else:
            self.health += 1

    def get_vis(self, world, time, maxX, maxY): #this function is so we have a uniform, square table to work w/ (including out of bounds)
        vis = np.full((maxX, maxY), water())
        relLeft = (self.x - self.sight)
        relRight = (self.x + self.sight)
        relUp = (self.y - self.sight)
        relDown = (self.y + self.sight)
        for x in range(maxX):
            for y in range(maxY):
                if x >= relLeft and x <= relRight and y >= relUp and y <= relDown:
                    if x >= 0 and x < maxX and y >= 0 and y < maxY:
                        vis[y, x] = world[x, y, time]
        return vis

    def process_vis(self, vis, maxX, maxY): #this one takes the table from get_vis() and turns it into a 1D table where each position is fixed relative to the creature
        newVis = []
        x = (self.x - 1)
        y = (self.y - 1)
        sideLen = 2
        for a in range(sightLim):
            for looper in range(4):
                if looper == 0:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(void())
                        x += 1
                elif looper == 1:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(void())
                        y += 1
                elif looper == 2:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(void())
                        x -= 1
                elif looper == 3:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(void())
                        y -= 1
                    x -= 1
                    y -= 1
                    sideLen += 2
        return newVis

class creatureTagger():
    def __init__(self):
        self.currentTag = 0

    def get_tag(self):
        self.currentTag += 1
        return self.currentTag

class matrix():
    def __init__(self, maxX = 1, maxY = 1, maxTime = 1):
        self.maxX = maxX
        self.maxY = maxY
        self.maxTime = maxTime
        self.matrix = np.full((maxX, maxY, maxTime), water())
        self.creatures = []
        self.foods = []
        self.hazards = []

    def copy_matrix(self, copyMatrix):
        newMatrix = matrix(self.maxX, self.maxY, self.maxTime)
        newMatrix.matrix = self.matrix
        newMatrix.creatures = self.creatures
        newMatrix.foods = self.foods
        newMatrix.hazards = self.hazards
        return newMatrix

    def move(self, creature, xDist, yDist, time):
        self.matrix[creature.x, creature.y, time + 1] = water()
        if xDist != 0:
            creature.moveX(xDist)
        if yDist != 0:
            creature.moveY(yDist)
        self.matrix[creature.x, creature.y, time + 1] = creature

    def move_Check(self, creature, xDist, yDist, time):
        if xDist == 0 and yDist == 0:
            self.move(creature, 0, 0, time)
            return
        #check position for type
        targetX = creature.x + xDist
        targetY = creature.y + yDist

        if targetX >= self.maxX or targetX < 0 or targetY >= self.maxY or targetY < 0:
            self.move(creature, 0, 0, time)
            return
        else:
            target = self.matrix[targetX, targetY, time + 1]

        #if creature, displace
        if target == 2:
            self.move(creature, 0, 0, time)
            return
        elif target == 3:
            self.move(creature, xDist, yDist, time)
            self.eat(self.foods, (creature.x, creature.y))
            self.nutrientCalculator(creature, (creature.x, creature.y))
            print("ate food at ", time)
            return
        else:
            self.move(creature, xDist, yDist, time)

    def eat(self, lists, pos):
        length = len(lists)
        for x in range(length):
            if lists[x].get_Pos()[0] == pos[0] and lists[x].get_Pos()[1] == pos[1]:
                del lists[x]
                return

    def poisonCalculator(self, creature, position, digestMax, digestMin):
        damage = 0
        #if food is out of edible range, determine poison damage
        #counting the distances between digestMin/Max and food's edibility number
        dist1 = dist2 = 0
        a = digestMax
        while a != self.foods[x].edibility:
            a = thousandCircle(a+1)
            dist1 += 1
        b = self.foods[x].edibility
        while b != digestMin:
            b = thousandCircle(b+1)
            dist2 += 1

        #dividing the max distance into 5 equal parts
        maxDist = (dist1 + dist2)/2
        i = maxDist % 5
        j = maxDist - i
        k = j / 5

        #determining which of digestMin/Max is closer
        smaller = None
        if dist1 > dist2:
            smaller = dist2
        elif dist1 < dist2:
            smaller = dist1
        else:
            smaller = dist1

        #determining which 5th the food lies on
        for fifth in range(1, 6):
            if smaller < (fifth * k):
                damage = fifth
                return damage
            elif smaller > j and smaller < maxDist:
                damage = i
                return damage

    def nutrientCalculator(self, creature, position):
        damage = 0
        #if a creature eats a food that isnt in its range it should take a slow effect or a poison effect based on how far it is from the eatable range
        digestMax = thousandCircle(creature.digestibility + creature.digestRange)
        digestMin = thousandCircle(creature.digestibility - creature.digestRange)

        #finding the food to be eaten and where on the circle it lies relative to the creature's food stats
        for x in range(len(self.foods)):
            if self.foods[x].get_Pos()[0] == position[0] and self.foods[x].get_Pos()[1] == position[1]:
                if self.foods[x].edibility <= digestMax and self.foods[x].edibility >= digestMin:
                    #if food is in edible range, add food
                    creature.add_food(abs(creature.digestibility - self.foods[x].edibility))
                elif self.foods[x].edibility <= digestMax or self.foods[x].edibility >= digestMin:
                    #if food is in edible range, add food
                    creature.add_food(abs(creature.digestibility - self.foods[x].edibility))
                elif self.foods[x].edibility <= digestMax and self.foods[x].edibility >= digestMin:
                    damage = self.poisonCalculator(creature, position, digestMax, digestMin)
                    creature.add_health(-damage)
                elif self.foods[x].edibility <= digestMax or self.foods[x].edibility >= digestMin:
                    damage = self.poisonCalculator(creature, position, digestMax, digestMin)
                    creature.add_health(-damage)
    def attack(self, creature, direction):
        pass

    def getVis(self, creature):
        pass

    def next_Second(self):
        pass

    def show_Vision(self, vis, maxX, maxY, time):
        for x in range(maxX):
            for y in range(maxY):
                if type(vis[x, y, time]) == water:
                    pass
                elif type(vis[x, y, time]) == creature:
                    pass
                elif type(vis[x, y, time]) == void:
                    pass

    def show_Matrix(self, xSize, ySize, maxTime):
        selected = None
        cursorX = cursorY = 0

        xScale = xSize/self.maxX
        yScale = ySize/self.maxY

        screen = pygame.display.set_mode((screenSizeX, screenSizeY), pygame.NOFRAME | pygame.FULLSCREEN)

        state = 2
        t=0
        while state == 2:
            mouse = pygame.mouse.get_pos()
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
                if key[pygame.K_q]:
                    state = 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse[0] <= xSize and mouse[1] <= ySize:
                        cursorX = math.floor(mouse[0])
                        cursorY = math.floor(mouse[1])
                        print(cursorX, cursorY)

                        creatureIndex = 0
                        for selector in self.creatures:
                            creatureIndex += 1
                            if self.matrix[cursorX, cursorY, t] == selector:
                                selected = selector
                                print("selected at", cursorX, cursorY)
                        if selected == None:
                            print("nothing selected at", cursorX, cursorY)
                        else:
                            print("creature tag:", selected.tag, " speed:", selected.speed, " food:", selected.food, " health:", selected.health)
                            print(selected.process_vis(selected.get_vis(self.matrix, t, self.maxX, self.maxY), self.maxX, self.maxY))
                            

                # if bob.health > 0:
                #    if key[pygame.K_SPACE]:
                #        copier = bob.get_vis(world, t)
                #        print(copier)
                #        visual = bob.process_vis(copier)
                #        print(visual)
                # keep this as a template
            #matrix drawing
            for x in range(self.maxX):
                for y in range(self.maxY):
                    if type(self.matrix[x, y, t]) == water:
                        pygame.draw.rect(screen, blue, (x * xScale, y * yScale, xScale, yScale))
                    elif type(self.matrix[x, y, t]) == creature:
                        pygame.draw.rect(screen, yellow, (x * xScale, y * yScale, xScale, yScale))
                    elif type(self.matrix[x, y, t]) == food:
                        pygame.draw.rect(screen, green, (x * xScale, y * yScale, xScale, yScale))
            #Sidebar drawing
            pygame.draw.rect(screen, white, (xSize+1, 0, 1920-xSize, 1080))
            if (1455+310) > mouse[0] > 1455 and (200+50) > mouse[1] > 200:
                pygame.draw.rect(screen, light_green, (1455, 200, 310, 50))
            else:
                pygame.draw.rect(screen, green, (1455, 200, 310, 50))

            pygame.display.flip()

def run(config_path):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #winner = p.run(eval_genomes, 50)

    # show final stats
    #print('\nBest genome:\n{!s}'.format(winner))

def main(genomes, config):
    nets = []
    ge = []
    creatures = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        creatures.append(creature(node()))
        g.fitness = 0
        ge.append(g)

    time = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

"""
notes:
- make a matrix class, move all of the collision detection into that and make
    it so the coder can decide the size of the matrix or choose from a set of
    pre-made sizes in initialization
- make a class for buttons and menus or something so that it's easy to make
- maybe make a test code for each function to test if it still works
"""