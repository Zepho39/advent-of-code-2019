import math
import csv
import itertools
import logging


# Takes a moon (array of 3 positional args) and list of moons
# Calculates the velocity of this moon for this step
# Returns the velocity to apply this step where velocity is an array of 3 args to apply to the x, y, and z value of the moon
def gravity(moon, listOfMoons, velocity):
	for m in listOfMoons:
		#print("DEBUG: gravity: for moon {} and m {} starting velocity = {}".format(moon, m, velocity))
		if tuple(m) != tuple(moon):
			if moon[0] > m[0]:
				velocity[0] = velocity[0] - 1
			elif moon[0] < m[0]:
				velocity[0] = velocity[0] + 1
			if moon[1] > m[1]:
				velocity[1] = velocity[1] - 1
			elif moon[1] < m[1]:
				velocity[1] = velocity[1] + 1
			if moon[2] > m[2]:
				velocity[2] = velocity[2] - 1
			elif moon[2] < m[2]:
				velocity[2] = velocity[2] + 1
		#print("DEBUG: gravity: for moon {} and m {} ending velocity = {}".format(moon, m, velocity))
	return velocity

def applyVelocity(moon, velocity):
	return [moon[0] + velocity[0], moon[1] + velocity[1], moon[2] + velocity[2]]

def getEnergy(moon, velocity):
	potential = sum(map(abs, moon))
	kinetic = sum(map(abs, velocity))
	return potential * kinetic

# Assumes the listOfMoons and listOfVelocity are in the same order of moons
def totalEnergy(listOfMoons, listOfVelocity):
	sumEnergy = 0
	for i in range(0, len(listOfMoons)):
		currentEnergy = getEnergy(listOfMoons[i], listOfVelocity[i])
		#print("DEBUG: totalEnergy: Energy for moon {} and velocity {} = {}".format(listOfMoons[i], listOfVelocity[i], currentEnergy))
		sumEnergy += currentEnergy
	return sumEnergy

def moonStep(listOfMoons, listOfVelocity):
	for i in range(0, len(listOfMoons)):
		listOfVelocity[i] = gravity(listOfMoons[i], listOfMoons, listOfVelocity[i])
	for i in range(0, len(listOfMoons)):
		listOfMoons[i] = applyVelocity(listOfMoons[i], listOfVelocity[i])
	return (listOfMoons, listOfVelocity)

def seedVelocity(moonCount):
	listOfVelocity = []
	for i in range(0, moonCount):
		listOfVelocity.append([0, 0, 0])
	return listOfVelocity

def simulateEnergy(steps, listOfMoons):
	listOfVelocity = seedVelocity(len(listOfMoons))
	step = 0
	while step < steps:
		#print("DEBUG: simulateEnergy: at step {} moons = {} and velocities = {}".format(step, listOfMoons, listOfVelocity))
		step += 1
		moonStepTuple = moonStep(listOfMoons, listOfVelocity)
		listOfMoons = moonStepTuple[0]
		listOfVelocity = moonStepTuple[1]
	energy = totalEnergy(listOfMoons, listOfVelocity)
	return energy 

def parseMoonFile(file):
	listOfMoons = []
	with open(file) as moons:
		moon = moons.readline()
		while moon:
			moon = moon.replace('=', ',').replace('<', '').replace('>', '').replace('\n', '')
			moonArray = moon.split(',')
			#print("DEBUG: parseMoonFile: moon = {}, moonArray = {}".format(moon, moonArray))
			listOfMoons.append([int(moonArray[1]), int(moonArray[3]), int(moonArray[5])])
			#print("DEBUG: parseMoonFile: input moon is {} and we added {} to the list".format(moon, listOfMoons[-1]))
			moon = moons.readline()
	return listOfMoons


def nBody1(file, steps):
	listOfMoons = parseMoonFile(file)
	energy = simulateEnergy(steps, listOfMoons)
	print("INFO: nBody1: Energy after {} steps: {}".format(steps, energy))


def nBody2(file):
	states = {}
	listOfMoons = parseMoonFile(file)
	listOfVelocity = seedVelocity(len(listOfMoons))
	steps = 0
	moonTuple = tuple(map(tuple, listOfMoons))
	velocityTuple = tuple(map(tuple, listOfVelocity))
	while not states.get((moonTuple, velocityTuple), False):
		#print(moonTuple)
		#print(velocityTuple)
		states[(moonTuple, velocityTuple)] = 1
		moonStepTuple = moonStep(listOfMoons, listOfVelocity)
		listOfMoons = moonStepTuple[0]
		listOfVelocity = moonStepTuple[1]
		moonTuple = tuple(map(tuple, listOfMoons))
		velocityTuple = tuple(map(tuple, listOfVelocity))
		steps += 1
	print("INFO: nBody2: Repeat moon state found after {} steps".format(steps))

#nBody1('aoc2019_12_1.input.txt', 1000)
nBody2('aoc2019_12_1.input.txt')







