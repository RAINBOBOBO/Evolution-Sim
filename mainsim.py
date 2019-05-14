import sys
import pygame
import os
import numpy as np

# import tensorflow as tf
# from tensorflow.keras import layers
# import keras

pygame.init()

# 0=null
# 1=water
# 2=creature
# 3=food
# 4=hazard
# 5=out of bounds

size = width, height = 500, 500
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
white = [255, 255, 255]

PROBABILITY_PERTURBING = 9

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


def dec(cre, world, time, foodlist, hazlist):
    num = np.random.randint(0, 4)
    eatType = 0
    if num == 0:
        eatType = cre.move_right(world, time, foodlist, hazlist)
    elif num == 1:
        eatType = cre.move_left(world, time, foodlist, hazlist)
    elif num == 2:
        eatType = cre.move_up(world, time, foodlist, hazlist)
    elif num == 3:
        eatType = cre.move_down(world, time, foodlist, hazlist)
    return eatType


def eat(lists, pos):
    print(lists)
    length = len(lists)
    for x in range(length):
        if lists[x][0] == pos[0] and lists[x][1] == pos[1]:
            del lists[x]
            print(lists)
            return
    print(lists)


def showGenome2(genome1):
    pygame.draw.rect(screen, white, (0, 0, 500, 500))
    coords = []
    ins = 0
    outs = 0
    hids = 0

    #1st loop through to get a count of each type to determine spacing
    for noder in genome1.get_nodeGenes().values():
        if (noder.get_type() == 0):
            ins += 1
        elif (noder.get_type() == 1):
            outs += 1
        elif (noder.get_type() == 2):
            hids += 1

    if ins != 0:
        inspace = 480/ins
    if outs != 0:
        outspace = 470/outs
    if hids != 0:
        hidspace = 425/hids
    icount = 0
    ocount = 0
    hcount = 0
    #2nd loop to assign coordinates
    #each entry has [id, type, x, y]
    for noder in genome1.get_nodeGenes().values():
        if (noder.get_type() == 0):
            entry = [noder.get_id(), 0, int(inspace * icount) + 20, 490]
            icount += 1
            coords.append(entry)
        elif (noder.get_type() == 1):
            entry = [noder.get_id(), 1, int(outspace * ocount) + 30, 10]
            ocount += 1
            coords.append(entry)
        elif (noder.get_type() == 2):
            entry = [noder.get_id(), 2, int(hidspace * hcount) + 75, 250]
            hcount += 1
            coords.append(entry)

    for nodedraw in coords:
        pygame.draw.circle(screen, blue, (nodedraw[2], nodedraw[3]), 10)

    for coner in genome1.get_connectionGenes().values():
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        for find in coords:
            if (coner.get_inNode() == find[0]):
                x1 = find[2]
                y1 = find[3]
            if (coner.get_outNode() == find[0]):
                x2 = find[2]
                y2 = find[3]
        if x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0:
            if coner.get_expressed():
                pygame.draw.line(screen, black, (x1,y1), (x2,y2))
        else:
            print("couldn't find nodes!!")


class food1():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = [x, y]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return self.pos


class hazard1():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = [x, y]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return self.pos


class node():
    def __init__(self, nextnode = None, prev = None, food1EC = None, resistance = None, x = None, y = None):
        self.nextnode = nextnode
        self.prev = prev
        self.food1EC = food1EC
        self.resistance = resistance
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

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

class creature():
    def __init__(self, Body1, speed = None, food = None, health = None, sight = None, actionPoints = None):
        self.Body1 = Body1
        self.speed = speed
        self.food = food
        self.health = health
        self.sight = sight
        self.actionPoints = actionPoints

    def get_Body(self):
        return self.Body1

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

    def add_food(self, amt = None):
        if (amt):
            self.food += amt
        else:
            self.food += 1

    def add_health(self, amt = None):
        if (amt):
            self.health += amt
        else:
            self.health += 1

    # for direction: 1=up, 2=right, 3=down, 4=left
    def can_move(self, direction, world, time):
        possible = False
        if direction == 1:
            if (self.Body1.getY() - self.speed) >= 0:
                if world[self.Body1.getX(), self.Body1.getY() - self.speed, time] != 2:
                    possible = True
        elif direction == 2:
            if (self.Body1.getX() + self.speed) <= (maxX - 1):
                if world[self.Body1.getX() + self.speed, self.Body1.getY(), time] != 2:
                    possible = True
        elif direction == 3:
            if (self.Body1.getY() + self.speed) <= (maxY - 1):
                if world[self.Body1.getX(), self.Body1.getY() + self.speed, time] != 2:
                    possible = True
        elif direction == 4:
            if (self.Body1.getX() - self.speed) >= 0:
                if world[self.Body1.getX() - self.speed, self.Body1.getY(), time] != 2:
                    possible = True
        return possible

    def move_right(self, world, time, foodlist, hazlist):
        eatType = 0
        if self.can_move(2, world, time) is True:
            if world[self.Body1.getX() + 1, self.Body1.getY(), time] == 3:
                self.add_food()
                eatType = 3
                eat(foodlist, (self.Body1.getX() + 1, self.Body1.getY()))
                print("eaten food ", self.food)
            elif world[self.Body1.getX() + 1, self.Body1.getY(), time] == 4:
                self.add_health(-1)
                eatType = 4
                eat(hazlist, (self.Body1.getX() + 1, self.Body1.getY()))
                print("eaten poison", self.health)
            if self.health <= 0:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveX(self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 3
            else:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveX(self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        else:
            world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        return eatType

    def move_left(self, world, time, foodlist, hazlist):
        eatType = 0
        if self.can_move(4, world, time) is True:
            if world[self.Body1.getX() - 1, self.Body1.getY(), time] == 3:
                self.add_food()
                eatType = 3
                eat(foodlist, (self.Body1.getX() - 1, self.Body1.getY()))
                print("eaten food ", self.food)
            elif world[self.Body1.getX() - 1, self.Body1.getY(), time] == 4:
                self.add_health(-1)
                eatType = 4
                eat(hazlist, (self.Body1.getX() - 1, self.Body1.getY()))
                print("eaten poison", self.health)
            if self.health <= 0:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveX(-self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 3
            else:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveX(-self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        else:
            world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        return eatType

    def move_up(self, world, time, foodlist, hazlist):
        eatType = 0
        if self.can_move(1, world, time) is True:
            if world[self.Body1.getX(), self.Body1.getY() - 1, time] == 3:
                self.add_food()
                eatType = 3
                eat(foodlist, (self.Body1.getX(), self.Body1.getY() - 1))
                print("eaten food ", self.food)
            elif world[self.Body1.getX(), self.Body1.getY() - 1, time] == 4:
                self.add_health(-1)
                eatType = 4
                eat(hazlist, (self.Body1.getX(), self.Body1.getY() - 1))
                print("eaten poison", self.health)
            if self.health <= 0:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveY(-self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 3
            else:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveY(-self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        else:
            world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        return eatType

    def move_down(self, world, time, foodlist, hazlist):
        eatType = 0
        if self.can_move(3, world, time) is True:
            if world[self.Body1.getX(), self.Body1.getY() + 1, time] == 3:
                self.add_food()
                eatType = 3
                eat(foodlist, (self.Body1.getX(), self.Body1.getY() + 1))
                print("eaten food ", self.food)
            elif world[self.Body1.getX(), self.Body1.getY() + 1, time] == 4:
                self.add_health(-1)
                eatType = 4
                eat(hazlist, (self.Body1.getX(), self.Body1.getY() + 1))
                print("eaten poison", self.health)
            if self.health <= 0:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveY(self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 3
            else:
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 1
                self.Body1.moveY(self.speed)
                world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        else:
            world[self.Body1.getX(), self.Body1.getY(), time + 1] = 2
        return eatType

    def get_vis(self, world, time):
        vis = np.full((maxX, maxY), 0)
        relLeft = (self.Body1.getX() - self.sight)
        relRight = (self.Body1.getX() + self.sight)
        relUp = (self.Body1.getY() - self.sight)
        relDown = (self.Body1.getY() + self.sight)
        for x in range(maxX):
            for y in range(maxY):
                if x >= relLeft and x <= relRight and y >= relUp and y <= relDown:
                    if x >= 0 and x < maxX and y >= 0 and y < maxY:
                        vis[y, x] = world[x, y, time]
        return vis

    def process_vis(self, vis):
        newVis = []
        x = (self.Body1.getX() - 1)
        y = (self.Body1.getY() - 1)
        sideLen = 2
        for a in range(sightLim):
            for looper in range(4):
                if looper == 0:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(5)
                        x += 1
                elif looper == 1:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(5)
                        y += 1
                elif looper == 2:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(5)
                        x -= 1
                elif looper == 3:
                    for traverser in range(sideLen):
                        if x >= 0 and x < maxX and y >= 0 and y < maxY:
                            newVis.append(vis[y, x])
                        else:
                            newVis.append(5)
                        y -= 1
                    x -= 1
                    y -= 1
                    sideLen += 2
        return newVis


class Genome():
    def __init__(self):
        self.connections = {}
        self.nodes = {}

    def addNodeGene(self, gene):
        self.nodes[gene.id] = gene

    def addConnectionGene(self, gene):
        self.connections[gene.innovationNum] = gene

    def get_connectionGenes(self):
        return self.connections

    def get_nodeGenes(self):
        return self.nodes

    def mutation(self):
        randy = np.random.random_sample(-2.0,2.0)
        perturb = np.random.randint(0,11)
        for con in self.connections.values():
            if (perturb > PROBABILITY_PERTURBING):
                con.set_weight(con.get_weight() * randy)
            else:
                con.set_weight(randy)

    def addConnectionMutation(self, innovation):
        randy = np.random.randint(0, len(self.nodes))
        node1 = self.nodes[randy]
        randy = np.random.randint(0, len(self.nodes))
        node2 = self.nodes[randy]
        tempWeight = np.randint(0, 1)

        isReversed = False
        if (node1.get_type() == 2 and node2.get_type() == 0):
            isReversed = True
        elif (node1.get_type() == 1 and node2.get_type() == 2):
            isReversed = True
        elif (node1.get_type() == 1 and node2.get_type() == 0):
            isReversed = True

        connectionExists = False
        for con in self.connections:
            if (self.connections[con].get_inNode() == node1.get_id() and self.connections[con].get_outNode() == node2.get_id()):
                connectionExists = True
                break
            elif (self.connections[con].get_inNode() == node2.get_id() and self.connections[con].get_outNode() == node1.get_id()):
                connectionExists = True
                break

        if (connectionExists):
            return

        tempIn = None
        tempOut = None
        if (isReversed):
            tempIn = node2
        else:
            tempIn = node1
        if (isReversed):
            tempOut = node1
        else:
            tempOut = node2

        tempCon = ConnectionGene(tempIn, tempOut, tempWeight, True, innovation.get_innovation())
        self.connections[tempCon.get_innovationNum()]

    def addNodeMutation(self, innovation):
        randy = np.random.randint(0, len(self.connections))
        con = self.connections[randy]

        inNode = self.nodes[con.get_inNode()]
        outNode = self.nodes[con.get_outNode()]

        con.disable()

        newNode = NodeGene(2, len(self.nodes)+1)
        inToNew = ConnectionGene(inNode.get_id(), newNode.get_id(), float(1), True, innovation.get_innovation())
        newToOut = ConnectionGene(newNode.get_id(), outNode.get_id(), con.get_weight(), True, innovation.get_innovation())

        self.nodes[newNode.get_id()] = newNode
        self.connections[inToNew.get_innovationNum()] = inToNew
        self.connections[newToOut.get_innovationNum()] = newToOut

    # parent1 fitness > parent2 fitness
    def crossover(self, parent1, parent2):
        child = Genome()

        for parent1Node in parent1.get_nodeGenes().values():
            child.addNodeGene(parent1Node.copy())

        for parent1Node in parent1.get_connectionGenes().values():
            if parent1Node.get_innovationNum() in parent2.get_connectionGenes():  # matching gene
                r = np.random.randint(0,2)
                if (r == 0):
                    childConGene = parent1Node.copy()
                else:
                    childConGene = parent2.get_connectionGenes()[parent1Node.get_innovationNum()].copy()
                child.addConnectionGene(childConGene)
            else:  # disjoint or excess gene
                childConGene = parent1Node.copy()
                child.addConnectionGene(childConGene)
        return child


class ConnectionGene():
    def __init__(self, inNode = None, outNode = None, weight = None, expressed = None, innovationNum = None):
        self.inNode = inNode
        self.outNode = outNode
        self.weight = weight
        self.expressed = expressed
        self.innovationNum = innovationNum

    def copy(self):
        newConnectionGene = ConnectionGene(self.inNode, self.outNode, self.weight, self.expressed, self.innovationNum)
        return newConnectionGene

    def get_inNode(self):
        return self.inNode

    def get_outNode(self):
        return self.outNode

    def get_weight(self):
        return self.weight

    def get_expressed(self):
        return self.expressed

    def get_innovationNum(self):
        return self.innovationNum

    def enable(self):
        self.expressed = True

    def disable(self):
        self.expressed = False

    def set_weight(self, newWeight):
        self.weight = newWeight



class NodeGene():
    def __init__(self, types = None, ids = None):
        """
        types can be: 
        0 = INPUT
        1 = OUTPUT
        2 = HIDDEN
        """
        self.type = types
        self.id = ids

    def copy(self):
        newNodeGene = NodeGene(self.type, self.id)
        return newNodeGene

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

class InnovationGenerator():
    def __init__(self):
        self.currentInnovation = 0

    def get_innovation(self):
        self.currentInnovation += 1
        return self.currentInnovation

# notes for bugfixes:
# make getters and setters and fix EVERYTHING
