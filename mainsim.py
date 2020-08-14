import sys
import pygame
from pygame.locals import *
import os
import numpy as np
import neat
from abc import ABC, abstractmethod
from fractions import Fraction
import math
import datetime

# import tensorflow as tf
# from tensorflow.keras import layers
# import keras

pygame.init()

print(sys.version)

# 0=null
# 1=water
# 2=creature
# 3=food
# 4=out of bounds

BLACK = [0, 0, 0]
RED = [200, 0, 0]
LIGHT_RED = [255, 0, 0]
GREEN = [0, 200, 0]
LIGHT_GREEN = [0, 255, 0]
BLUE = [0, 0, 200]
LIGHT_BLUE = [0, 0, 255]
ORANGE = [200, 110, 0]
LIGHT_ORANGE = [255, 110, 0]
YELLOW = [255, 255, 0]
WHITE = [255, 255, 255]
MENU_BLUE = [0, 100, 200]

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
myFont = pygame.font.SysFont("arial", 15)
SIGHTLIM = 3  # the hard cap, in matrix units (MU's now) of how far someone can see
clock = pygame.time.Clock()
FPS = 60
SCREEN_SIZE_Y = 1080
SCREEN_SIZE_X = 1920
seed = 15
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

def quitgame():
    pygame.quit()
    quit()

def timeup(t):
    if t < 29:
        t += 1
    return t

def timedown(t):
    if t > 0:
        t -= 1
    return t

def changeState0(state):
    state = 0
    return state

def changeState1(state):
    state = 1
    return state

def changeState2(state):
    state = 2
    return state

def changeState3(state):
    state = 3
    return state

def changeState4(state):
    # print("changeState4 ran")
    state = 4
    return state

def changeState5(state):
    state = 5
    return state

def setTrue(state):
    state = True
    return

def setFalse(state):
    state = False
    return

def setNone(state):
    state = None
    return state

def stateHandler(matrix, x, y, time, defaultState = 1):
    # print("inside stateHandler")
    done = False
    state = defaultState
    while done == False:
        if state == 1:
            state = menu()
        elif state == 2:
            state = matrix.show_Matrix(x, y, time)
        elif state == 3 or state == 4 or state == 5:
            # print("state is 3, done is True")
            done = True
    return state

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def menu():
    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME | pygame.FULLSCREEN)
    state = 1

    button_start = ButtonClass("start")
    button_menu_quit = ButtonClass("menuQuit")

    while state == 1:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if key[pygame.K_q]:
                quitgame()
        mouse = pygame.mouse.get_pos()

        #drawing the menu elements
        screen.fill(MENU_BLUE)
        largeText = pygame.font.SysFont("arial", 115)
        textSurf, textRect = text_objects('Evolution Simulator', largeText)
        textRect.center = (int(1920/2), int(1080/2))
        screen.blit(textSurf, textRect)

        #menu buttons
        state = button_start.button("Start", 810, 695, 300, 50, BLUE, LIGHT_BLUE, screen, changeState2, state)
        button_menu_quit.button("Quit", 810, 770, 300, 50, RED, LIGHT_RED, screen, quitgame)

        pygame.display.flip()
        clock.tick(FPS)
    return state

class SliderClass:
    def __init__(self, sliderID, x, y, w, h, barWidth, ac, screen, p1):
        self.id = sliderID
        self.mouseDown = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ac = ac
        self.screen = screen
        self.p1 = p1
        self.barWidth = barWidth
        self.sliderX = self.x + self.barWidth
        self.initialX = self.sliderX

    def slider(self, maxX, maxY):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #checking if mouse is in positon and clicking
        if (self.x + self.w) > mouse[0] > (self.x) and (self.y+self.h) > mouse[1] > self.y:
            if click[0] == 1:
                self.mouseDown = True
        if self.mouseDown and self.x < self.sliderX < (self.x + self.w):
            self.sliderX = mouse[0]
        if self.mouseDown == True and click[0] == 0:
            self.mouseDown = False
        if self.sliderX <= self.x:
            self.sliderX = self.x + self.barWidth
        elif self.sliderX >= (self.x + self.w):
            self.sliderX = (self.x + self.w) - 10

        #changing the value based on slider pos
        self.p1 = round((self.sliderX - self.x)/(self.w - 10) + 1, 2)
        
        #drawing the slider
        pygame.draw.rect(self.screen, self.ac, (self.x, self.y, self.barWidth, self.h))                             #left bar
        pygame.draw.rect(self.screen, self.ac, (self.sliderX, self.y, self.barWidth, self.h))                       #slider bar
        pygame.draw.rect(self.screen, self.ac, ((self.x + self.w - self.barWidth), self.y, self.barWidth, self.h))  #right bar
        pygame.draw.rect(self.screen, self.ac, (self.x, self.y + int(self.h/2), self.w, int(self.h/6)))                   #long bar

        #drawing the value for the slider
        timeText = pygame.font.SysFont("arial", 15)
        textSurf, textRect = text_objects(str(self.p1), timeText)
        textRect.center = ((self.x + self.w - self.barWidth) + 20, self.y + 10)
        self.screen.blit(textSurf, textRect)

        return self.p1


class ButtonClass:
    def __init__(self, buttonID):
        self.id = buttonID
        self.mouseDown = False

    def button(self, msg, x, y, w, h, ic, ac, screen, action = None, p1 = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #check if mouse is in position
        if (x+w) > mouse[0] > x and (y+h) > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1:
                self.mouseDown = True
            if self.mouseDown == True and action != None and click[0] == 0:
                self.mouseDown = False
                if p1 != None:
                    p1 = action(p1)
                else:
                    action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        #drawing the text on the button
        smallText = pygame.font.SysFont("arial", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = (int(x+(w/2)), int(y+(h/2)))
        screen.blit(textSurf, textRect)

        #return only if we have something to return
        if p1 != None:
            return p1


class Water:
    def __init__(self):
        self.fitID = 1


class Void:
    def __init__(self):
        self.fitID = 2


class Food:
    def __init__(self, x, y, edibility = None):
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.edibility = edibility
        self.fitID = 3

    def get_Pos(self):
        return self.pos


class Creature:
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
        self.fitID = 4
        self.hunger = 10

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

    def get_vis(self, world, time, maxX, maxY, creatureX, creatureY): #this function is so we have a uniform, square table to work w/ (including out of bounds)
        vis = np.full((maxX, maxY), Void()) #check if this should be void, not water... wat de fak?
        relLeft = (creatureX - self.sight)
        relRight = (creatureX + self.sight)
        relUp = (creatureY - self.sight)
        relDown = (creatureY + self.sight)
        for x in range(maxX):
            for y in range(maxY):
                if x >= relLeft and x <= relRight and y >= relUp and y <= relDown:
                    if x >= 0 and x < maxX and y >= 0 and y < maxY:
                        vis[x, y] = world[x, y, time]
        return vis

    def process_vis(self, world, time, maxX, maxY, creatureX, creatureY): #this one takes the table from get_vis() and turns it into a 1D table where each position is fixed relative to the creature
        vis = self.get_vis(world, time, maxX, maxY, creatureX, creatureY)
        newVis = []
        x = (self.x - 1)
        y = (self.y - 1)
        sideLen = 2
        for a in range(SIGHTLIM):
            for looper in range(4):
                if looper == 0:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[x, y])
                        else:
                            newVis.append(Void())
                        x += 1
                elif looper == 1:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[x, y])
                        else:
                            newVis.append(Void())
                        y += 1
                elif looper == 2:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[x, y])
                        else:
                            newVis.append(Void())
                        x -= 1
                elif looper == 3:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[x, y])
                        else:
                            newVis.append(Void())
                        y -= 1
                    x -= 1
                    y -= 1
                    sideLen += 2
        return newVis


class CreatureTagger:
    def __init__(self):
        self.currentTag = 0

    def get_tag(self):
        self.currentTag += 1
        return self.currentTag


class Matrix:
    def __init__(self, maxX = 1, maxY = 1, maxTime = 1):
        self.maxX = maxX
        self.maxY = maxY
        self.maxTime = maxTime
        self.matrix = np.full((maxX, maxY, maxTime), Water())
        self.creatures = []
        self.foods = []
        self.hazards = []

    def copy_matrix(self, copyMatrix):
        newMatrix = Matrix(self.maxX, self.maxY, self.maxTime)
        newMatrix.matrix = self.matrix
        newMatrix.creatures = self.creatures
        newMatrix.foods = self.foods
        newMatrix.hazards = self.hazards
        return newMatrix

    def move(self, creature, xDist, yDist, time):
        self.matrix[creature.x, creature.y, time + 1] = Water()
        if xDist != 0:
            creature.moveX(xDist)
        if yDist != 0:
            creature.moveY(yDist)
        self.matrix[creature.x, creature.y, time + 1] = creature

    def apply_Hunger(self, nets, ge, creatureList):
        for creature in creatureList:
            creature.hunger -= 1;
        listLength = len(creatureList)
        index = 0
        while index < listLength:
            if creatureList[index].hunger <= 0:
                creatureList.pop(index)
                nets.pop(index)
                ge.pop(index)
                listLength -= 1
            index += 1

    def move_Check(self, creature, xDist, yDist, time, genome):
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
            self.nutrientCalculator(creature, (creature.x, creature.y), genome)
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

    def nutrientCalculator(self, creature, position, genome):
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
                    genome.fitness += 5
                    creature.hunger += 3
                elif self.foods[x].edibility <= digestMax or self.foods[x].edibility >= digestMin:
                    #if food is in edible range, add food
                    creature.add_food(abs(creature.digestibility - self.foods[x].edibility))
                    genome.fitness += 5
                    creature.hunger += 3
                elif self.foods[x].edibility <= digestMax and self.foods[x].edibility >= digestMin:
                    damage = self.poisonCalculator(creature, position, digestMax, digestMin)
                    creature.add_health(-damage)
                    genome.fitness -= 15
                elif self.foods[x].edibility <= digestMax or self.foods[x].edibility >= digestMin:
                    damage = self.poisonCalculator(creature, position, digestMax, digestMin)
                    creature.add_health(-damage)
                    genome.fitness -= 15
    def attack(self, creature, direction):
        pass

    def getVis(self, creature):
        pass

    def next_Second(self):
        pass

    def show_Vision(self, xPos, yPos, vis, maxX, maxY, time, screen):
        xScale =  math.ceil(600/self.maxX)
        yScale =  math.ceil(600/self.maxY)
        for x in range(maxX):
            for y in range(maxY):
                if type(vis[x, y]) == Water:
                    pygame.draw.rect(screen, BLUE, (xPos + (x * xScale), yPos + (y * yScale), xScale, yScale))
                elif type(vis[x, y]) == Creature:
                    pygame.draw.rect(screen, YELLOW, (xPos + (x * xScale), yPos + (y * yScale), xScale, yScale))
                elif type(vis[x, y]) == Food:
                    pygame.draw.rect(screen, GREEN, (xPos + (x * xScale), yPos + (y * yScale), xScale, yScale))
                elif type(vis[x, y]) == Void:
                    pygame.draw.rect(screen, RED, (xPos + (x * xScale), yPos + (y * yScale), xScale, yScale))

    def show_Matrix(self, xSize, ySize, maxTime):
        selected = None
        prevSelected = None
        cursorX = cursorY = 0
        play = 0
        a = 0
        playSpeed = 1

        xScale = math.ceil(xSize/self.maxX)
        yScale = math.ceil(ySize/self.maxY)

        screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y), pygame.NOFRAME | pygame.FULLSCREEN)

        state = 2
        t=0
        prevT = None

        #defining buttons
        button_play = ButtonClass("play")
        button_pause = ButtonClass("pause")
        button_back = ButtonClass("back")
        button_quit = ButtonClass("quit")
        button_tUp = ButtonClass("tUp")
        button_tDown = ButtonClass("tDown")
        button_menu = ButtonClass("menu")
        button_unselect = ButtonClass("unselect")
        button_nextGen = ButtonClass("nextGen")
        button_5Gen = ButtonClass("5Gen")
        button_10Gen = ButtonClass("10Gen")

        slider_time = SliderClass("time", 1455, 380, 310, 20, 5, GREEN, screen, playSpeed)

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
                        cursorX = math.floor(mouse[0]/xScale)
                        cursorY = math.floor(mouse[1]/yScale)

                        creatureIndex = 0
                        for selector in self.creatures:
                            creatureIndex += 1
                            if self.matrix[cursorX, cursorY, t] == selector:
                                selected = selector
                                print("selected at", cursorX, cursorY)
                        if selected == None:
                            print("nothing selected at", cursorX, cursorY)
                        else:
                            print("creature tag:", selected.tag, " speed:", selected.speed, " food:", selected.food, " health:", selected.health, "time:", t)
                            #print(selected.process_vis(self.matrix, t, self.maxX, self.maxY, cursorX, cursorY))

            #matrix drawing
            if prevT != None and prevT != t:
                for x in range(self.maxX):
                    for y in range(self.maxY):
                        if type(self.matrix[x, y, t]) == Water:
                            pygame.draw.rect(screen, BLUE, (x * xScale, y * yScale, xScale, yScale))
                        elif type(self.matrix[x, y, t]) == Creature:
                            pygame.draw.rect(screen, YELLOW, (x * xScale, y * yScale, xScale, yScale))
                        elif type(self.matrix[x, y, t]) == Food:
                            pygame.draw.rect(screen, GREEN, (x * xScale, y * yScale, xScale, yScale))
            if prevT == None:
                for x in range(self.maxX):
                    for y in range(self.maxY):
                        if type(self.matrix[x, y, 0]) == Water:
                            pygame.draw.rect(screen, BLUE, (x * xScale, y * yScale, xScale, yScale))
                        elif type(self.matrix[x, y, 0]) == Creature:
                            pygame.draw.rect(screen, YELLOW, (x * xScale, y * yScale, xScale, yScale))
                        elif type(self.matrix[x, y, 0]) == Food:
                            pygame.draw.rect(screen, GREEN, (x * xScale, y * yScale, xScale, yScale))

            if selected != None:
                if prevSelected == None or prevSelected != selected:
                    pygame.draw.rect(screen, WHITE, (self.maxX*xScale, 0, 1920-xSize, 1080))
                    selectedText = pygame.font.SysFont("arial", 20)
                    textSurf, textRect = text_objects("creature tag:" + (str(selected.tag) + ", speed:" + str(selected.speed) + ", food:" + str(selected.food) + ", health:" + str(selected.health)) + " at t = " + str(t) + ", (" + str(cursorX) + "," + str(cursorY) + ")",  selectedText)
                    textRect.center = (1580, 200)
                    screen.blit(textSurf, textRect)

                    tempVis = selected.get_vis(self.matrix, t, self.maxX, self.maxY, cursorX, cursorY)
                    
                    self.show_Vision(1320, 480, tempVis, self.maxX, self.maxY, t, screen)

            prevT = t
            
            #buttons
            if selected == None:
                pygame.draw.rect(screen, WHITE, (self.maxX*xScale, 0, 1920-xSize, 1080))
                play = button_play.button("Play", 1455, 200, 310, 50, GREEN, LIGHT_GREEN, screen, changeState1, play)
                play = button_pause.button("Pause", 1455, 260, 310, 50, GREEN, LIGHT_GREEN, screen, changeState0, play)
                t = button_back.button("Back", 1455, 320, 310, 50, GREEN, LIGHT_GREEN, screen, changeState0, t)
                t = button_tUp.button("Time -1", 1455, 600, 150, 50, BLUE, LIGHT_BLUE, screen, timedown, t)
                t = button_tDown.button("Time +1", 1610, 600, 150, 50, BLUE, LIGHT_BLUE, screen, timeup, t)
                playSpeed = slider_time.slider(self.maxX, self.maxY)
                state = button_nextGen.button("New Generation", 1455, 780, 310, 50, ORANGE, LIGHT_ORANGE, screen, changeState3, state)
                state = button_5Gen.button("5Gen", 1455, 840, 310, 50, ORANGE, LIGHT_ORANGE, screen, changeState4, state) #maybe a unique state for each option, then run function for 5 gen in main
                state = button_10Gen.button("10Gen", 1455, 900, 310, 50, ORANGE, LIGHT_ORANGE, screen, changeState5, state)
                state = button_menu.button("Menu", 1455, 960, 310, 50, MENU_BLUE, LIGHT_BLUE, screen, changeState1, state)
                button_quit.button("Quit", 1455, 1020, 310, 50, RED, LIGHT_RED, screen, quitgame)

                # print("inside show matrix, state is", state)

                #when play button is pressed
                if play == 1 and t < (maxTime-1):
                    a += playSpeed
                    if a >= 50:
                        a = 0
                        t += 1

                #displaying stats
                timeText = pygame.font.SysFont("arial", 20)
                textSurf, textRect = text_objects(str(t), timeText)
                textRect.center = (1900, 1060)
                screen.blit(textSurf, textRect)
                
            else:
                selected = button_unselect.button("Back", 1455, 400, 310, 50, GREEN, LIGHT_GREEN, screen, setNone, selected)

            prevSelected = selected

            pygame.display.flip()
            clock.tick(FPS)
        # print("leaving show matrix, again state is ", state)
        return state


class StateTracker:
    def __init__(self, initial_state = 1):
        self.state = initial_state
        self.generation_ran = False
        self.buffer = 0
   
    def set_state(self, state):
        self.state = state

    def run_once(self):
        if self.generation_ran:
            self.generation_ran = False
            self.state = 2
        else:
            self.generation_ran = True

    def run_x_times(self, x):
        # print("run_x_times ran")
        if self.buffer < x:
            self.buffer += 1
        else:
            self.buffer = 0
            self.state = 2




def new_Gen(newMatrix, creatureList): #make this accept a list of creatures as a param, then load it into matrix
    newMatrix.matrix = np.full((newMatrix.maxX, newMatrix.maxY, newMatrix.maxTime), Water())
    newMatrix.foods = []
    newMatrix.creatures = []
    foodCount = 10
    for x in range(foodCount):
        temp = Food(np.random.randint(0, newMatrix.maxX), np.random.randint(0, newMatrix.maxY))
        newMatrix.foods.append(temp)

    for x in range(len(creatureList)):
        newMatrix.creatures.append(creatureList[x])

    #loading into matrix
    for foodloader in range(foodCount):
        newMatrix.matrix[newMatrix.foods[foodloader].get_Pos()[0], newMatrix.foods[foodloader].get_Pos()[1], 0] = newMatrix.foods[foodloader]

    for creatureLoader in range(len(creatureList)):
        if type(newMatrix.matrix[newMatrix.creatures[creatureLoader].x, newMatrix.creatures[creatureLoader].y, 0]) == Food:
            print("creature ate at ", newMatrix.creatures[creatureLoader].x, newMatrix.creatures[creatureLoader].y)
            newMatrix.creatures[creatureLoader].add_food()
            newMatrix.eat(newMatrix.foods, (newMatrix.creatures[creatureLoader].x, newMatrix.creatures[creatureLoader].y))
            foodCount -= 1
        newMatrix.matrix[newMatrix.creatures[creatureLoader].x, newMatrix.creatures[creatureLoader].y, 0] = newMatrix.creatures[creatureLoader]

    return newMatrix

def new_Seed(currentDT):
    newSeed = (currentDT.minute * currentDT.microsecond + currentDT.year * currentDT.hour * currentDT.second)
    return newSeed


def run(config_path, str1):
    """
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

    # print("before main")
    winner = p.run(main, 50)

    # show final stats
    #print('\nBest genome:\n{!s}'.format(winner))

main_state = StateTracker()
def main(genomes, config):
    # print("running main", genomes, config)
    nets = []
    ge = []
    creatures = []
    maxX = maxY = 30
    maxTime = 30
    SIGHTLIM = 3  # the hard cap, in matrix units (MU's now) of how far someone can see
    clock = pygame.time.Clock()
    # main_state = 1 #uncomment to show functionality
    FPS = 60
    currentDT = datetime.datetime.now()
    size = width, height = 1300, 1080

    creatureTagGenerator = CreatureTagger()
    creatureCount = 10
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        creatures.append(Creature(creatureTagGenerator.get_tag(), 1, 0, 1, 1, None, np.random.randint(0, 1001), np.random.randint(10, 101), np.random.randint(0, maxX), np.random.randint(0, maxY)))
        g.fitness = 0
        ge.append(g)

    time = 0
    
    generation = 1
    run = True
    while run:
        # print('mainloopstart')
        clock.tick(FPS)
        newMatrix = Matrix(maxX, maxY, maxTime)
        newMatrix = new_Gen(newMatrix, creatures)

        # print("04040404")
        if len(creatures) == 0:
            run = False
            break
        # print("05050505")

        for time in range(maxTime-1):
            for fooder in newMatrix.foods:
                newMatrix.matrix[fooder.get_Pos()[0], fooder.get_Pos()[1], time + 1] = newMatrix.matrix[fooder.get_Pos()[0], fooder.get_Pos()[1], time]

            for g in ge:
                pass

            for i, creer in enumerate(newMatrix.creatures):
                tempVis = creer.process_vis(newMatrix.matrix, time, maxX, maxY, creer.x, creer.y)
                if creer.health <= 0:
                    creatures.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                    continue

                #come up w/ a better solution, maybe while loops or decrememnting i maybe
                if (len(ge) > i):
                    ge[i].fitness += 1
                else:
                    continue

                output = nets[i].activate((creer.x, creer.y, tempVis[0].fitID,  tempVis[1].fitID, tempVis[2].fitID,  tempVis[3].fitID,  tempVis[4].fitID,  tempVis[5].fitID,  tempVis[6].fitID,  tempVis[7].fitID)) #whatever vis is, pass in some of the vision data
                # print("06060606")
                if output[0] < 0.2:
                    newMatrix.move_Check(creer, 0, 0, time, ge[i])
                elif output[0] > 0.2 and output[0] < 0.4:
                    newMatrix.move_Check(creer, creer.speed, 0, time, ge[i])
                elif output[0] > 0.4 and output[0] < 0.6:
                    newMatrix.move_Check(creer, -creer.speed, 0, time, ge[i])
                elif output[0] > 0.6 and output[0] < 0.8:
                    newMatrix.move_Check(creer, 0, creer.speed, time, ge[i])
                elif output[0] > 0.8:
                    newMatrix.move_Check(creer, 0, -creer.speed, time, ge[i])

                newMatrix.apply_Hunger(nets, ge, creatures)

                # decisionX = dec()
                # decisionY = dec()
                # xDist = 0
                # yDist = 0
                # if decisionX == 0:
                #     xDist += creer.speed
                # elif decisionX == 1:
                #     xDist -= creer.speed
                # if decisionY == 0:
                #     yDist += creer.speed
                # elif decisionY == 1:
                #     yDist -= creer.speed
                # newMatrix.move_Check(creer, xDist, yDist, time, ge[i])

        # print("main_state is ", main_state.state, " before going into stateHandler.")
        main_state.set_state(stateHandler(newMatrix, size[0], size[1], maxTime, main_state.state))
        # print("main_state is ", main_state.state, " after going into stateHandler.")

        #if main_state = 3, run once, if 4, run 5 times, if 5, run 10 times
        if main_state.state == 3:
            main_state.run_once()
        elif main_state.state == 4:
            # print("button successfully set state to 4.")
            main_state.run_x_times(5)
        elif main_state.state == 5:
            main_state.run_x_times(10)
        print(generation)
        generation += 1
        del newMatrix


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path, "test2")

"""
notes:
- make a matrix class, move all of the collision detection into that and make
    it so the coder can decide the size of the matrix or choose from a set of
    pre-made sizes in initialization
- make a class for buttons and menus or something so that it's easy to make
- maybe make a test code for each function to test if it still works
- https://youtu.be/dQw4w9WgXcQ

solution for fitness function:
1. State handler returns the state (3 if new gen is pressed) when it finishes.
2. Save that number to be passed into the next state handler call, so that we can skip the menu
"""